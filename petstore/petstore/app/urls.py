from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name="index"),
    path("singup/",views.singup,name="singup"),
    path("singin/",views.singin,name="singin"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("petdetail/<int:petid>/",views.petdetail,name="petdetail"),
]
