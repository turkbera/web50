# Generated by Django 4.2.3 on 2023-07-17 09:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_alter_auction_category_delete_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='auction',
            name='isOpen',
            field=models.BooleanField(default='True'),
        ),
    ]
