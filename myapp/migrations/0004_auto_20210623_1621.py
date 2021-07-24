# Generated by Django 3.2.4 on 2021-06-23 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_auto_20210623_1438'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproducts',
            name='img',
            field=models.ImageField(blank=True, null=True, upload_to='products'),
        ),
        migrations.AddField(
            model_name='allproducts',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='allproducts',
            name='unit',
            field=models.CharField(default='-', max_length=200),
        ),
    ]
