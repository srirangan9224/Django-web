# Generated by Django 5.0.6 on 2024-07-05 18:29

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("network", "0004_remove_post_person_post_profile"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="likes",
            field=models.ManyToManyField(
                related_name="likes", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="Like",
        ),
    ]
