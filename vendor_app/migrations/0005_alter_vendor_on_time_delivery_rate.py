# Generated by Django 5.0.4 on 2024-05-08 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vendor_app', '0004_historicalperformance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='on_time_delivery_rate',
            field=models.FloatField(default=0.0),
        ),
    ]