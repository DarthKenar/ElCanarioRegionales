# Generated by Django 4.1.3 on 2023-07-18 19:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_alter_dollargraph_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='dollargraph',
            options={'ordering': ['id'], 'verbose_name': 'Dollar price', 'verbose_name_plural': 'Dollar prices'},
        ),
    ]
