from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("singup/",views.singup,name="singup"),
    path("singin/",views.singin,name="singin")
]
