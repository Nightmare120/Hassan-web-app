# Generated by Django 4.2.2 on 2023-07-06 14:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ReactAdmin', '0007_project_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='creator',
            field=models.TextField(default='{"username":"mk","password":"123456"}'),
            preserve_default=False,
        ),
    ]
