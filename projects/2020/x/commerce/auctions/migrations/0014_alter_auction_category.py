# Generated by Django 4.2.3 on 2023-07-17 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.TextField(blank=True, null='True'),
        ),
    ]
