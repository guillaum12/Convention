# Generated by Django 4.2.3 on 2023-12-23 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0017_choice_parent_categorie'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='color',
            field=models.CharField(default='#000000', max_length=7),
        ),
    ]
