from django.shortcuts import render,HttpResponse, redirect
from .models import Pet
from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
# Create your views here.


def index(req):
    allpets=Pet.objects.all()
    # petdata=Pet.objects.filter(petname="Rocky")
    # print(petdata)
    return render(req,"index.html", {"allpets":allpets}) 

from django.core.exceptions import ValidationError

def validate_password(password):
    if len(password) < 8 and len(password) > 128:
        raise ValidationError("Password must be atleast long and less than 128")
    has_upper=False
    has_lower=False
    has_digit=False
    has_special=False
    specialchars="@$!%?&"

    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in specialchars:
            has_special = True


    if not has_upper:
        raise ValidationError("Password must contain atleast one uppercase letter")
    elif not has_lower:
            raise ValidationError("Password must contain atleast one upperlowercase letter")
    if not has_digit:
            raise ValidationError("Password must contain atleast one digit letter")
    if not has_special:
            raise ValidationError("Password must contain atleast one special char (e.g. @$!%?&)")
    
    commonpassword=["password","123456","qwerty","abc123"]
    if password in commonpassword:
        raise ValidationError("This password is too common.please chose another one.")


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
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req,"singup.html",context) 
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

from django.contrib import messages
from django.db.models import Q
def searchpets(req):
    query=req.GET["q"]
    print(query)
    allpets = Pet.objects.filter(Q(petname__icontains=query) | Q(description__icontains=query))
    print(allpets,len(allpets))
    if len(allpets) == 0:
        messages.error(req, "No result found!!")
    context = {"allpets": allpets}
    if req.user.is_authenticated:
        return render(req, "dashboard.html", context)
    else:
        return render(req, "index.html", context)

def searchbygender(req):
    gender=req.GET["gender"]
    if gender=="male":
        allpets = Pet.objects.filter(gender__exact="Male")
    else:
        allpets = Pet.objects.filter(gender__exact="Female")
    context = {"allpets":allpets}
    print(allpets)
    if req.user.is_authenticated:
        return render(req, "dashboard.html", context)
    else:
        return render(req, "index.html", context)

def req_password(req):
    if req.method == "POST":
        uemail = req.POST["uemail"]
        try:
            user = User.objects.get(email=uemail)
            # return render(req,"reset_password.html",{"uemail":user.email})
            return redirect("reset_password",uemail=user.email)
        except User.DoesNotExist:
            messages.error(req,"No account found with this email")
            return render(req, "reqpassword.html")
    else:
        return render(req, "reqpassword.html")
    
def reset_password(req,uemail):
    user = User.objects.get(email=uemail)
    if req.method == "POST":
        upass=req.POST["upass"]
        ucpass=req.POST["ucpass"]
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req,"singup.html",context) 
        if upass != ucpass:
            messages.error(req,"Confirm password and Password do not match")
            return render(req,"reset_password.html",{"uemail":uemail})
        else:
            user.set_password(upass)
            user.save()
            return redirect("singin")
    else:
        return render(req,"reset_password.html",{"uemail":uemail})