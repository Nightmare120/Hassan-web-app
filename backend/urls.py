"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path
from ReactAdmin import views

urlpatterns = [
    path('admin/', admin.site.urls),
    re_path('login',views.login),
    re_path('user/create',views.create_user),
    re_path('overview',views.get_overview),
    re_path('user/all',views.all_user),

    re_path('user/delete',views.delete_user),
    re_path('respondent/get',views.get_respondent),
    re_path('respondent/save',views.save_respondent),
    re_path('respondent/view_conversation',views.view_conversation),
    
    # to be  check
    re_path('respondent/delete',views.delete_respondent),
    
    # all project releated backend
    re_path('project/all',views.get_projects),
    re_path('project/create',views.create_project_by_excel),
    re_path('project/single',views.get_single_project),
    
    re_path('project/update',views.update_project),
    re_path('project/respondent',views.get_project_respondent),
    re_path('project/questions',views.get_questions),
    re_path('project/delete',views.delete_project),
    re_path('project/*',views.show_chat),
    re_path('',views.show_admin)
    
    # to be made
    # delete project
    # change status of project
    #* update question
    #* and images in project
    # re_path('respondent/create',views.get_respondent)
]
