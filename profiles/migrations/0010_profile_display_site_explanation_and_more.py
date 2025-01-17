# Generated by Django 5.0.2 on 2024-02-28 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0009_profile_is_banned'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='display_site_explanation',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='category',
            field=models.CharField(choices=[('etudiant', 'Étudiant/e'), ('administration', 'Administration'), ('association', 'Association'), ('convention', 'Soirée Convention Étudiante')], default='etudiant', max_length=50),
        ),
    ]
