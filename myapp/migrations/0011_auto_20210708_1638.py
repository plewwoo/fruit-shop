# Generated by Django 3.2.4 on 2021-07-08 16:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0010_rename_allproducts_allproduct'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(max_length=100)),
                ('productId', models.CharField(max_length=100)),
                ('productName', models.CharField(max_length=100)),
                ('price', models.IntegerField()),
                ('quantity', models.IntegerField()),
                ('total', models.IntegerField()),
            ],
        ),
        migrations.RenameField(
            model_name='cart',
            old_name='ProductName',
            new_name='productName',
        ),
        migrations.CreateModel(
            name='OrderPending',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderId', models.CharField(max_length=100)),
                ('name', models.CharField(max_length=100)),
                ('tel', models.CharField(max_length=100)),
                ('address', models.TextField()),
                ('shipping', models.CharField(max_length=100)),
                ('payment', models.CharField(max_length=100)),
                ('ps', models.TextField()),
                ('stamp', models.DateTimeField(auto_now_add=True, null=True)),
                ('paid', models.BooleanField(default=False)),
                ('slip', models.ImageField(blank=True, null=True, upload_to='slip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
