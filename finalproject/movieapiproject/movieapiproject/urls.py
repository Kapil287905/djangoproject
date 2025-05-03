"""
URL configuration for movieapiproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import path
from app.views import Allmovie,Addmovie,Updatemovie,Deletemovie 
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.apioverview),
    path('Allmovie/',Allmovie.as_view(),name='Allmovie'),
    path('Addmovie/',Addmovie.as_view(),name='Addmovie'),
    path('Updatemovie/update/<int:pk>',Updatemovie.as_view(),name='Updatemovie'),
    path('Deletemovie/delete/<int:pk>',Deletemovie.as_view(),name='Deletemovie'),
    path('searchbycategory/',views.searchbycategory,name='searchbycategory'),
]
