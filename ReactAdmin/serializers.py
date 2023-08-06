from rest_framework import serializers
from .models import Respondent, Project
from django.contrib.auth.models import User

class RespondentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Respondent 
        fields = ('id', 'name', 'project', 'date', 'conversation')

class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project 
        fields = ('id', 'name', 'audience_age', 'desc','status','total_respondent','current_respondent', 'allow_images','questions','url','creator')
