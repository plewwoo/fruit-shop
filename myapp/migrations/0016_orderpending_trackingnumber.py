# Generated by Django 3.2.4 on 2021-07-22 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_orderpending_sliptime'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderpending',
            name='trackingNumber',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
