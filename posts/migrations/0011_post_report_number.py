# Generated by Django 4.2.3 on 2023-12-17 18:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0010_post_theme'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='report_number',
            field=models.IntegerField(default=0),
        ),
    ]