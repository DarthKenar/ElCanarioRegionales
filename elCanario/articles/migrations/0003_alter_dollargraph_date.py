# Generated by Django 4.1.3 on 2023-07-18 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_dollargraph_alter_article_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dollargraph',
            name='date',
            field=models.DateField(auto_now_add=True),
        ),
    ]
