# Generated by Django 2.1.1 on 2018-09-29 14:48

from django.conf import settings
import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("contenttypes", "0002_remove_content_type_name"),
        ("common", "0010_auto_20180929_1052"),
    ]

    operations = [
        migrations.CreateModel(
            name="LogEntry",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("object_id", models.PositiveIntegerField(db_index=True)),
                ("datetime", models.DateTimeField(auto_now_add=True, db_index=True)),
                ("action_type", models.CharField(max_length=255)),
                ("data", django.contrib.postgres.fields.jsonb.JSONField(null=True)),
                (
                    "content_type",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to="contenttypes.ContentType",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={"ordering": ("-datetime", "-id")},
        )
    ]