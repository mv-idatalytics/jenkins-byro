# Generated by Django 1.11.8 on 2018-02-26 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("documents", "0001_initial")]

    operations = [
        migrations.AddField(
            model_name="document",
            name="title",
            field=models.CharField(max_length=300, null=True),
        )
    ]
