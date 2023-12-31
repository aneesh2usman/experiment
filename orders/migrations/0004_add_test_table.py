# Generated by Django 4.2.3 on 2023-07-24 09:35

from django.db import migrations, models
import django.db.models.deletion
import psqlextra.manager.manager


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0003_add_update_table"),
    ]

    operations = [
        migrations.CreateModel(
            name="LineItem2",
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
                ("name", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product2",
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
                ("name", models.TextField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "lineItem2",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="orders.lineitem2",
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
    ]
