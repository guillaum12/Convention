# Generated by Django 4.2.3 on 2023-12-30 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0008_profile_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_banned',
            field=models.BooleanField(default=False),
        ),
    ]
