# Generated by Django 4.2.3 on 2023-07-17 12:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auction_isopen'),
    ]

    operations = [
        migrations.AddField(
            model_name='bid',
            name='isAccepted',
            field=models.BooleanField(default='False'),
        ),
    ]