# Generated by Django 3.1.7 on 2021-10-06 00:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_product_bids'),
    ]

    operations = [
        migrations.AlterField(
            model_name='buyer',
            name='profile_img',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
