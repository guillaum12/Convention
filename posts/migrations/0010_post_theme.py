# Generated by Django 4.2.3 on 2023-12-09 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_choice'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='theme',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='posts.choice'),
            preserve_default=False,
        ),
    ]
