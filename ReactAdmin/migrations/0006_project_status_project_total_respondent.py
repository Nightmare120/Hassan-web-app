# Generated by Django 4.2.2 on 2023-06-29 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactAdmin', '0005_project'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='status',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='project',
            name='total_respondent',
            field=models.IntegerField(default=0),
        ),
    ]