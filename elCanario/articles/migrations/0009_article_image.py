# Generated by Django 4.2.4 on 2023-08-30 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0008_article_stock_delete_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image',
            field=models.ImageField(null=True, upload_to='articles'),
        ),
    ]
