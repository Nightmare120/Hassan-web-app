from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import *
from .models import Respondent
from django.contrib.auth import authenticate
from django.http import JsonResponse
from .Excel_handler import extract_from_excel, generate_api_project
import os
from django.shortcuts import render
import json
from .Keyword_handler import get_conversation_with_keywords

def show_chat(request):
    return render(request,"chatpage.html")

def show_admin(request):
    return render(request,"index.html")

# Create your views here.
@api_view(['GET'])
def get_overview(request):
    if request.method == 'GET':
        project = Project.objects.all().count()
        respondent = Respondent.objects.all().count()
        coworker = User.objects.all().count()

        data = {"project": project, "respondent": respondent, "coworker":coworker}
        
        return JsonResponse(data,safe = False)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

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
        'name' : request.data['name'] , 'project' : request.data['project'], 'date' : request.data['date'], 'conversation' : json.dumps(get_conversation_with_keywords(json.loads(request.data['conversation'])))
    }

    print(data)

    serializer = RespondentSerializer(data=data)
    project =  Project.objects.get(name=request.data['project'])
    
    if serializer.is_valid() and project.current_respondent < project.total_respondent:
        serializer.save()
        project.current_respondent = project.current_respondent + 1
        project.save(update_fields=['current_respondent'])
        
        project.url =  project.url + str(project.current_respondent) 
        project.save(update_fields=['url'])

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
def delete_project(request):
    if request.method == 'POST':
        id = request.data['id']
        print(Project.objects.filter(id=id))
        Project.objects.filter(id=id).delete()
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
        dataOfUser = json.loads(request.POST['user_details'])
        username = dataOfUser['username']
        password = dataOfUser['password']
        print(dataOfUser)
        data = {
            'name': request.POST['name'],
            'audience_age' : request.POST['audience'],
            'desc' : request.POST['desc'],
            'total_respondent':request.POST['total_respondent'],
            'allow_images': convertIntoPythonBoolean(request.POST['allowImgVideos']),
            'questions' : extract_from_excel(request.FILES['file']),
            'url': generate_api_project(),
            'creator': f'"username":"{username}","password":"{password}"'
        }
        serializer = ProjectSerializer(data=data)
        if serializer.is_valid():
            serializer.save()

        return Response(status=status.HTTP_200_OK)
    
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def convertIntoPythonBoolean(value):
    if value == "true":
        return True
    else:
        return False

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

@api_view(['POST'])
def save_files(request):
        if request.method == "POST":
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
    

@api_view(['POST'])
def get_projects(request):
    if request.method == 'POST':
        username = request.data['username']
        password = request.data['password']

        if not check_for_superuser(username,password):
            # query = json.dumps({"username": username, "password": password})
            print(f'"username":"{username}","password":"{password}"')
            data = Project.objects.filter(creator=f'"username":"{username}","password":"{password}"')
            serializer = ProjectSerializer(data, context={'request': request}, many=True)
            return Response(serializer.data)

        data = Project.objects.all()

        serializer = ProjectSerializer(data, context={'request': request}, many=True)

        return Response(serializer.data)
    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

def check_for_superuser(username,password):
    user  = authenticate(username=username, password=password)
        # print(user.password)
    return User.objects.get(username=user.get_username(),password=user.password).is_superuser

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