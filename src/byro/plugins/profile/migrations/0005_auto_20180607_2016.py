# Generated by Django 1.11.13 on 2018-06-07 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profile", "0004_auto_20171206_1919")]

    operations = [
        migrations.AlterField(
            model_name="memberprofile",
            name="birth_date",
            field=models.DateField(blank=True, null=True, verbose_name="Birth date"),
        ),
        migrations.AlterField(
            model_name="memberprofile",
            name="nick",
            field=models.CharField(
                blank=True, max_length=200, null=True, verbose_name="Nick"
            ),
        ),
    ]