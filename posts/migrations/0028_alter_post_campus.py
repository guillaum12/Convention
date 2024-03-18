# Generated by Django 4.2.5 on 2024-03-18 16:01

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0027_alter_post_campus"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="campus",
            field=models.CharField(
                choices=[
                    ("--", "--"),
                    ("Saclay", "Saclay"),
                    ("Rennes", "Rennes"),
                    ("Metz", "Metz"),
                ],
                default="Saclay",
                max_length=10,
            ),
        ),
    ]
