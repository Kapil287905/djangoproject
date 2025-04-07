from django.urls import path
from . import views
from app.views import PetRegister,PetUpdate,PetDelete

urlpatterns = [
    path("",views.index,name="index"),
    path("singup/",views.singup,name="singup"),
    path("singin/",views.singin,name="singin"),
    path("dashboard/",views.dashboard,name="dashboard"),
    path("userlogout/",views.userlogout,name="userlogout"),
    path("petdetail/<int:petid>/",views.petdetail,name="petdetail"),
    path("PetRegister/",PetRegister.as_view(),name="PetRegister"),
    path("PetUpdate/<int:pk>/",PetUpdate.as_view(),name="PetUpdate"),
    path("PetDelete/<int:pk>/",PetDelete.as_view(),name="PetDelete"),
    path("searchpets",views.searchpets,name="searchpets"),
    path("searchbygender",views.searchbygender,name="searchbygender"),
]
