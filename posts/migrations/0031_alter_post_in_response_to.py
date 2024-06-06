# Generated by Django 4.2.5 on 2024-06-03 10:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("posts", "0030_post_is_troll"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="in_response_to",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="posts.post",
            ),
        ),
    ]