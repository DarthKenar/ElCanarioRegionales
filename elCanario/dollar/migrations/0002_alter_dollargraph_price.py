# Generated by Django 4.2.3 on 2023-07-26 06:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dollar', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dollargraph',
            name='price',
            field=models.FloatField(),
        ),
    ]
