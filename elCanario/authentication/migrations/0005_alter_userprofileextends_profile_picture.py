# Generated by Django 4.2.4 on 2023-08-30 04:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_alter_userprofileextends_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileextends',
            name='profile_picture',
            field=models.ImageField(blank=True, default='', null=True, upload_to='static/img/profile-pictures/'),
        ),
    ]