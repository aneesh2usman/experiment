# Generated by Django 4.2.3 on 2023-07-24 05:23

import compositefk.fields
import datetime
from django.db import migrations, models
import django.db.models.deletion
import orders.models
import psqlextra.backend.migrations.operations.add_default_partition
import psqlextra.backend.migrations.operations.create_partitioned_model
import psqlextra.manager.manager
import psqlextra.models.partitioned
import psqlextra.types
from psqlextra.backend.migrations.operations import PostgresAddRangePartition


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
    ]

    operations = [
        psqlextra.backend.migrations.operations.create_partitioned_model.PostgresCreatePartitionedModel(
            name="Product",
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
                ("lineitem_id", models.IntegerField()),
                ("created", models.DateTimeField(auto_now_add=True)),
                (
                    "date_range",
                    models.DateField(default=datetime.date.today, verbose_name="Date"),
                ),
                (
                    "order",
                    orders.models.CustomCompositeForeignKey(
                        null_if_equal=[],
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="lineItem",
                        to="orders.order",
                        to_fields={
                            "date_range": compositefk.fields.LocalFieldValue(
                                "date_range"
                            ),
                            "id": compositefk.fields.LocalFieldValue("lineitem_id"),
                        },
                    ),
                ),
            ],
            options={
                "abstract": False,
                "base_manager_name": "objects",
            },
            partitioning_options={
                "method": psqlextra.types.PostgresPartitioningMethod["RANGE"],
                "key": ["date_range"],
            },
            bases=(psqlextra.models.partitioned.PostgresPartitionedModel,),
            managers=[
                ("objects", psqlextra.manager.manager.PostgresManager()),
            ],
        ),
        psqlextra.backend.migrations.operations.add_default_partition.PostgresAddDefaultPartition(
            model_name="Product",
            name="default",
        ),
        PostgresAddRangePartition(
           model_name="product",
           name="product_2023_01_01_to_2023_12_31",
           from_values='2023-01-01',
           to_values='2023-12-31',
        ),
        PostgresAddRangePartition(
           model_name="product",
           name="product_2024_01_01_to_2024_12_31",
           from_values='2024-01-01',
           to_values='2024-12-31',
        ),
        PostgresAddRangePartition(
           model_name="product",
           name="product_2025_01_01_to_2025_12_31",
           from_values='2025-01-01',
           to_values='2025-12-31',
        ),
        migrations.AlterField(
            model_name="lineitem",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="order",
            name="created",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
