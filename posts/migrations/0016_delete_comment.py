# Generated by Django 4.2.3 on 2023-12-23 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0015_alter_post_theme'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Comment',
        ),
    ]