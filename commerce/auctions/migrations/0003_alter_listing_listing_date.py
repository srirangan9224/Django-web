# Generated by Django 4.1.7 on 2024-05-18 11:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_listing_watchlist_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='listing_date',
            field=models.DateTimeField(default=datetime.datetime(2024, 5, 18, 16, 54, 0, 898614)),
        ),
    ]