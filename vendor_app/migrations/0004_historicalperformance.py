# Generated by Django 5.0 on 2023-12-08 07:30

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendor_app", "0003_purchaseorder"),
    ]

    operations = [
        migrations.CreateModel(
            name="HistoricalPerformance",
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
                ("date", models.DateTimeField(default=django.utils.timezone.now)),
                ("on_time_delivery_rate", models.FloatField(blank=True, null=True)),
                ("quality_rating_avg", models.FloatField(blank=True, null=True)),
                ("average_response_time", models.FloatField(blank=True, null=True)),
                ("fulfillment_rate", models.FloatField(blank=True, null=True)),
                (
                    "vendor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="vendor_app.vendor",
                    ),
                ),
            ],
        ),
    ]
