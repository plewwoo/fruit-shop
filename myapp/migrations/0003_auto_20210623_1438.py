# Generated by Django 3.2.4 on 2021-06-23 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_allproducts_imgurl'),
    ]

    operations = [
        migrations.AddField(
            model_name='allproducts',
            name='instock',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='allproducts',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
