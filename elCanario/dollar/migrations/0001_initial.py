# Generated by Django 4.2.4 on 2023-08-25 19:40

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DollarGraph',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.FloatField()),
                ('date', models.DateField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Dollar price',
                'verbose_name_plural': 'Dollar prices',
                'ordering': ['id'],
            },
        ),
    ]
