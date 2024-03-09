# Generated by Django 5.0.2 on 2024-02-29 19:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0023_choice_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='choice',
            name='image',
            field=models.ImageField(blank=True, default='generic_theme.jpg', upload_to='themes', validators=[django.core.validators.FileExtensionValidator(['png', 'jpg', 'jpeg'])]),
        ),
    ]