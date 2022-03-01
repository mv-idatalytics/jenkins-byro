# Generated by Django 1.11.13 on 2018-06-26 18:08

from django.db import migrations


def migrate_bookkeeping_model(apps, schema_editor):
    # In the old model, the bank account was implicit. Most VirtualTransaction
    # that have "None" set as source or destination account refer to the bank
    # account here. Except the automatic member fee bookings.
    #
    # Steps:
    #  1. Generate/Find standard accounts: bank, fees_receivable, fees,  donations
    #  2. Find all RealTransaction and process them
    #    a. RealTransaction with VirtualTransaction objects map directly to
    #       new Transaction objects
    #    b. RealTransaction with no VirtualTransaction map to a new unbalanced
    #       Transaction, referencing the bank account
    #  3. Regenerate 'reverses' relation on the new objects
    #  4. Find VirtualTransaction that have not been processed in step 2
    #    a. If they reference a 'member_fees' account, turn them into Transactions
    #       between fees, fees_receivable, and bank, as appropriate
    #    b. Otherwise they probably shouldn't exist, turn them into unbalanced
    #       Transactions
    #
    from byro.bookkeeping.special_accounts import SpecialAccounts

    Account = apps.get_model("bookkeeping", "Account")
    VirtualTransaction = apps.get_model("bookkeeping", "VirtualTransaction")
    RealTransaction = apps.get_model("bookkeeping", "RealTransaction")
    Transaction = apps.get_model("bookkeeping", "Transaction")
    Booking = apps.get_model("bookkeeping", "Booking")

    bank = SpecialAccounts.bank
    fees_receivable = SpecialAccounts.fees_receivable
    fees = SpecialAccounts.fees
    donations = SpecialAccounts.donations

    ACCOUNT_MAP = {"member_donation": donations, "member_fees": fees_receivable}
    map_account = lambda account: ACCOUNT_MAP.get(account.account_category, account)

    handled_vts = set()
    rt_mapping = {}
    for rt in RealTransaction.objects.all():
        t = Transaction.objects.create(
            booking_datetime=rt.booking_datetime, value_datetime=rt.value_datetime
        )
        rt_mapping[rt.pk] = t.pk
        if rt.amount > 0:
            booking = t.bookings.create(debit_account_id=bank.id, amount=rt.amount)
        else:
            booking = t.bookings.create(credit_account_id=bank.id, amount=-rt.amount)
        booking.data = {}
        booking.booking_datetime = rt.booking_datetime
        booking.source = rt.source
        booking.importer = rt.importer
        booking.memo = rt.purpose
        booking.data["other_party"] = rt.originator
        if rt.importer.endswith("csv_importer"):
            booking.data["csv_line"] = rt.data
        elif rt.data:
            booking.data["generic_data"] = rt.data
        booking.save()

        for vt in rt.virtual_transactions.all():
            params = {
                "member": vt.member,
                "amount": vt.amount,
                "data": {"_migration_value_datetime": str(vt.value_datetime)},
            }
            if vt.destination_account:
                t.bookings.create(
                    credit_account_id=map_account(vt.destination_account).id, **params
                )
            if vt.source_account:
                t.bookings.create(
                    debit_account_id=map_account(vt.source_account).id, **params
                )
            handled_vts.add(vt.pk)

    for rt in RealTransaction.objects.filter(reverses__isnull=False).all():
        t = Transaction.objects.get(pk=rt_mapping[rt.pk])
        t.reverses = Transaction.objects.get(pk=rt_mapping[rt.reverses.pk])
        t.save()

    for vt in VirtualTransaction.objects.exclude(pk__in=handled_vts).all():
        t = Transaction.objects.create(value_datetime=vt.value_datetime)

        params = {"member": vt.member, "amount": vt.amount}

        if vt.source_account and vt.destination_account:
            # Special case: Balanced VirtualTransaction
            #  (nothing in the code base generates these, handle them anyway)
            t.bookings.create(
                credit_account_id=map_account(vt.destination_account).id, **params
            )
            t.bookings.create(
                debit_account_id=map_account(vt.source_account).id, **params
            )
        elif vt.source_account and vt.source_account.account_category == "member_fees":
            # Member fee liability
            t.bookings.create(credit_account_id=fees.id, **params)
            t.bookings.create(debit_account_id=fees_receivable.id, **params)

        elif (
            vt.destination_account
            and vt.destination_account.account_category == "member_fees"
        ):
            # Member fee payment, f.e. from make_testdata
            t.bookings.create(credit_account_id=fees_receivable.id, **params)
            t.bookings.create(debit_account_id=bank.id, **params)

        elif vt.source_account:
            # Something else
            t.bookings.create(
                credit_account_id=map_account(vt.source_account).id, **params
            )

        elif vt.destination_account:
            # Something else
            t.bookings.create(
                debit_account_id=map_account(vt.source_account).id, **params
            )

        else:
            # A VirtualTransaction with no source or destination account is a sure sign of multiple exclamation marks
            raise Exception(
                "Migration error: {} without either source or destination account!!!!!".format(
                    vt
                )
            )


class Migration(migrations.Migration):

    dependencies = [
        ("bookkeeping", "0012_auto_20180617_1926"),
        ("common", "0013_logentry_logchain"),
    ]

    operations = [
        migrations.RunPython(migrate_bookkeeping_model, migrations.RunPython.noop)
    ]