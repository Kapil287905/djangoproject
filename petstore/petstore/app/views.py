from django.shortcuts import render,HttpResponse, redirect
from .models import Pet
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
# Create your views here.


def index(req):
    allpets=Pet.objects.all()
    return render(req,"index.html", {"allpets":allpets}) 


def singup(req):    
    if req.method == "GET":
        print(req.method) # GET
        return render(req,"singup.html")
    else:
        print(req.method) # POST
        uname=req.POST["uname"]
        uemail=req.POST["uemail"]
        upass=req.POST["upass"]
        ucpass=req.POST["ucpass"]
        print(uname,upass,ucpass,uemail)
        if upass != ucpass:
            errmsg="Password and Confirm password nust be same"
            context = {"errmsg":errmsg}
            return render(req,"singup.html",context)
        elif uname == upass:
            errmsg="Password should not be same as email id"
            context = {"errmsg":errmsg}
            return render(req,"singup.html",context)
        else:
            try:
                userdata=User.objects.create(username=uname,email=uemail,password=upass)
                userdata.set_password(upass)
                userdata.save()
                print(User.objects.all())
                return redirect("singin")
            except:
                errmsg="User already exist. Try with different username"
                context = {"errmsg":errmsg}
                return render(req,"singup.html",context)
        

def singin(req):
    if req.method == "GET":
        print(req.method) # GET
        return render(req,"singin.html")
    else:
        uname=req.POST["uname"]
        upass=req.POST["upass"]
        print(upass,uname)
        # userdata=User.objects.filter(email=uemail,password=upass)
        userdata = authenticate(username=uname,password=upass)
        print(userdata)
        if userdata is not None:
            login(req,userdata)
            # return render(req, "dashboard.html")
            return redirect("dashboard")
        else:
            context = {}
            context["errmsg"] = "Invalid email or password"
            return render(req,"singin.html",context)
        
def dashboard(req):
    print(req.user)
    username = req.user
    allpets=Pet.objects.all()
    print(allpets)
    return render(req, "dashboard.html",{"username": username,"allpets":allpets})

def userlogout(req):
    logout(req)
    return redirect('/')

def petdetail(req,petid):
    petdata=Pet.objects.get(petid=petid)
    context={'petdata':petdata}
    return render(req, "petdetail.html",context)

from .forms import PetForm
from django.views.generic.edit import CreateView,UpdateView,DeleteView
from django.views.generic.list import ListView

class PetRegister(CreateView):
    model = Pet
    fields = "__all__"
    success_url = "/dashboard"

class PetUpdate(UpdateView):
    model = Pet
    template_name_suffix="_update_form"
    fields = "__all__"
    success_url = "/dashboard"

class PetDelete(DeleteView):
    model = Pet
    success_url = "/dashboard"






