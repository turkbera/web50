# Generated by Django 4.2.3 on 2023-07-16 23:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0009_category_alter_auction_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='category',
            field=models.CharField(choices=[('food', 'Food'), ('fashion', ' Fashion'), ('personalCare', 'Personal Care'), ('software', 'Software'), ('home', 'Home and Kitchen'), ('electronics', 'Electronics'), ('book', 'Book'), ('others', 'Others')], max_length=20),
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]
