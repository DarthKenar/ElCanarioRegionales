# Generated by Django 4.2.4 on 2023-10-30 11:58

import customers.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_alter_customer_address_alter_customer_dni_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customer',
            name='email',
            field=models.EmailField(blank=True, max_length=50, null=True, unique=True, validators=[customers.models.allowed_emails]),
        ),
    ]
