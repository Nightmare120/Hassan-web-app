# Generated by Django 4.2.2 on 2023-08-06 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactAdmin', '0009_project_current_respondent'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='allow_images',
            field=models.BooleanField(default=False),
        ),
    ]
