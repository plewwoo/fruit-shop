# Generated by Django 3.2.4 on 2021-07-12 17:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0012_orderpending_paymentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderpending',
            name='ps',
            field=models.TextField(blank=True, null=True),
        ),
    ]
