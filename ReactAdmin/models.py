from django.db import models

# Create your models here.
class Respondent(models.Model):
    name = models.CharField("Name", max_length=240)
    project = models.CharField(max_length=240)
    date = models.CharField(max_length=240)
    conversation = models.TextField()

class Project(models.Model):
    name = models.CharField(max_length=240)
    audience_age = models.CharField(max_length=240)
    desc = models.CharField(max_length=500)
    status = models.IntegerField(default=0)
    total_respondent = models.IntegerField(default=0)
    current_respondent = models.IntegerField(default=0)
    allow_images = models.BooleanField(default=False)
    questions = models.TextField()
    url = models.CharField(max_length=500)
    creator = models.TextField()
