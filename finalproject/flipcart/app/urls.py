from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("signup/", views.signup, name="signup"),
    path("signin/", views.signin, name="signin"),
    path("req_password/", views.req_password, name="req_password"),
    path("reset_password/<uemail>/", views.reset_password, name="reset_password"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path('searchproduct/',views.searchproduct,name='searchproduct')
]
