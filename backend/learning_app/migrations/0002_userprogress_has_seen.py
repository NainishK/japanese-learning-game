# Generated by Django 4.2.6 on 2024-11-23 20:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('learning_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='has_seen',
            field=models.BooleanField(default=False),
        ),
    ]
