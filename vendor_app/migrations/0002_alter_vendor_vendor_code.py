# Generated by Django 5.0 on 2023-12-07 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="vendor",
            name="vendor_code",
            field=models.CharField(max_length=20, unique=True),
        ),
    ]
