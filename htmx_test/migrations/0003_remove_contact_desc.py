# Generated by Django 4.2.3 on 2023-08-03 05:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("htmx_test", "0002_contact_desc"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="contact",
            name="desc",
        ),
    ]
