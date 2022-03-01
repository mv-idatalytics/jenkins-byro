# Generated by Django 2.0 on 2017-12-06 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("bookkeeping", "0006_remove_account_member")]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="account_category",
            field=models.CharField(
                choices=[
                    ("member_donation", "Donation account"),
                    ("member_fees", "Membership fee account"),
                    ("asset", "Asset account"),
                    ("liability", "Liability account"),
                    ("income", "Income account"),
                    ("expense", "Expense account"),
                ],
                max_length=15,
            ),
        )
    ]
