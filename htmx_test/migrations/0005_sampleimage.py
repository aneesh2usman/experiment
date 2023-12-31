# Generated by Django 4.2.4 on 2023-08-14 07:15

from django.db import migrations, models
import vehicle_tracking.fields


class Migration(migrations.Migration):

    dependencies = [
        ("htmx_test", "0004_apikey"),
    ]

    operations = [
        migrations.CreateModel(
            name="SampleImage",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image",
                    vehicle_tracking.fields.Base64ImageField(
                        blank=True, null=True, upload_to="images/"
                    ),
                ),
            ],
        ),
    ]
