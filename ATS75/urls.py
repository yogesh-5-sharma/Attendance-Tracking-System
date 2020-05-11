"""projects URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views as myview

app_name="ATS75"
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name="ATS75/login.html"), name='login'),
    path('logout/' , auth_views.logout_then_login , name='logout'),
    path('signup/' , myview.signup , name='signup' ),
    #
    path('', myview.home , name='home'),
    #
    path('addschedule/' , myview.add_schedule , name='add_schedule' ),
    #
    path('deleteschedule/', myview.delete_schedule , name='delete_schedule'),
    #
    path('addsubject/', myview.add_subject , name='add_subject'),
    #
    path('myattendancerecord/' , myview.show_attendance_record , name='show_attendance_record')
]
