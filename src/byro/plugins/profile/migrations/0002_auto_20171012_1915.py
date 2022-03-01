# Generated by Django 1.11.6 on 2017-10-12 19:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("profile", "0001_initial")]

    operations = [
        migrations.RemoveField(model_name="memberprofile", name="address"),
        migrations.RemoveField(model_name="memberprofile", name="member_identifier"),
        migrations.RemoveField(model_name="memberprofile", name="name"),
        migrations.AddField(
            model_name="memberprofile",
            name="phone_number",
            field=models.CharField(blank=True, max_length=32, null=True),
        ),
    ]