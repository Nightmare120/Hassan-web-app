from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import Respondent
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .Excel_handler import extract_from_excel
import os
from django.shortcuts import render

def show_chat(request):
    return render(request,"chatpage.html")

def show_admin(request):
    return render(request,"index.html")

# Create your views here.
@api_view(['GET'])
def get_respondent(request):
    if request.method == 'GET':
        data = Respondent.objects.all()

        serializer = RespondentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def save_respondent(request):

    data = {
        'name' : request.data['name'] , 'project' : request.data['project'], 'date' : request.data['date'], 'conversation' : request.data['conversation']
    }

    print(data)

    serializer = RespondentSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_201_CREATED)

    return Response(status=status.HTTP_103_EARLY_HINTS)

#? incomplet but works
@api_view(['POST'])
def view_conversation(request):
    if request.method == 'POST':
        id = request.data['id']
        data = Respondent.objects.filter(id=id)
        serializer = RespondentSerializer(data, context={'request': request}, many=True)
        return Response(serializer.data)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def delete_respondent(request):
    if request.method == 'POST':
        id = request.data['id']
        print(Respondent.objects.filter(id=id))
        Respondent.objects.filter(id=id).delete()
        return Response(status=status.HTTP_200_OK)
   
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        user = authenticate(username=request.data['username'], password=request.data['password'])
        if user is not None:
            return Response(status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
   
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def create_user(request):
    if request.method == 'POST':
        username = request.data['username']
        email = request.data['email']
        password = request.data['password']
        User.objects.create_user(username, email, password)
        return Response(status=status.HTTP_200_OK)
   
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def delete_user(request):
    if request.method == 'POST':
        id = request.data['id']
        print(User.objects.filter(id=id))
        User.objects.filter(id=id).delete()
        return Response(status=status.HTTP_200_OK)
   
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['GET'])
def all_user(request):
    data = list(User.objects.values())
    return JsonResponse(data,safe = False)
   
@api_view(['POST'])
def create_project_by_excel(request):
    if request.method == "POST":
        data = {
            'name': request.POST['name'],
            'audience_age' : request.POST['audience'],
            'desc' : request.POST['desc'],
            'questions' : extract_from_excel(request.FILES['file'])
        }
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


@api_view(['POST'])
def update_project(request):
    if request.method == "POST":
        print(request.POST)
        
        id = request.POST['id']
        question = request.POST['question']
        
        project =  Project.objects.get(id=id)
        project.questions = question
        project.save(update_fields=['questions'])

        for file in request.FILES:
            write_project_file(path=file,f=request.FILES[file])
            print(file,request.FILES[file],end="\n\n")
        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def write_project_file(path,f):
    directry = get_directory(path)
    print("dir", directry)
    if  not os.path.isdir(f"./static/{directry}") :
        os.mkdir(f"./static/{directry}")
    
    with open(f"./static/{path}", "wb+") as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def get_directory(path):
    print(path)
    print("splited path",str(path).split("/"))
    return str(path).split("/")[0]
    

@api_view(['GET'])
def get_projects(request):
    if request.method == 'GET':
        data = Project.objects.all()

        serializer = ProjectSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

@api_view(['POST'])
def get_project_respondent(request):
     if request.method == 'POST':
        project = request.data['name']
        data = Respondent.objects.filter(project=project)

        serializer = RespondentSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)

@api_view(['POST'])
def  get_single_project(request):
    if request.method == 'POST':
        id = request.data['id']
        
        serializer = ProjectSerializer(Project.objects.get(id=id), context={'request': request})
        return Response(serializer.data)

    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    
@api_view(["POST"])
def get_questions(request):
    print(request.data)
    if request.method == 'POST':
        key = request.data['key']
        serializer = ProjectSerializer(Project.objects.get(url=key), context={'request': request})
        return Response(serializer.data)