from django.shortcuts import render,redirect
from .models import UserDetail,Products,Carts,Orders,Payments
from django.contrib.auth.models import User

# Create your views here.
def index(req):
    return render(req,"index.html") 

from django.core.exceptions import ValidationError


def validate_password(password):
    if len(password) < 8 or len(password) > 128:
        raise ValidationError(
            "Password must be atleast 8 character long and less than 128"
        )

    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    specialchars = "@$!%*?&"

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
        raise ValidationError("Password must contain at least one uppercase letter")

    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter")

    if not has_digit:
        raise ValidationError("Password must contain at least one digit letter")

    if not has_special:
        raise ValidationError(
            "Password must contain at least one special char (e.g. @$!%*?&)"
        )

    commonpassword = ["password", "123456", "qwerty", "abc123"]
    if password in commonpassword:
        raise ValidationError("This password is too common. Please choose another one.")


def signup(req):
    if req.method == "GET":
        print(req.method)  # GET
        return render(req, "signup.html")
    else:
        print(req.method)  # POST
        uname = req.POST["uname"]
        uemail = req.POST["uemail"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        print(uname, upass, ucpass, uemail)
        context = {}
        try:
            validate_password(upass)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context)

        if upass != ucpass:
            errmsg = "Password and Confirm password must be same"
            context = {"errmsg": errmsg}
            return render(req, "signup.html", context)
        elif uname == upass:
            errmsg = "Password should not be same as email id"
            context = {"errmsg": errmsg}
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(
                    username=uname, email=uemail, password=upass
                )
                userdata.set_password(upass)
                userdata.save()
                print(User.objects.all())
                return redirect("signin")
            except:
                errmsg = "User already exists. Try with different username"
                context = {"errmsg": errmsg}
                return render(req, "signup.html", context)


from django.contrib.auth import authenticate, login, logout


def signin(req):
    if req.method == "GET":
        print(req.method)
        return render(req, "signin.html")
    else:
        uname = req.POST.get("uname")
        uemail = req.POST.get("uemail")
        upass = req.POST["upass"]
        print(uname, uemail, upass)
        # userdata = User.objects.filter(email=uemail, password=upass)
        userdata = authenticate(username=uname, email=uemail, password=upass)
        print(userdata)  # if matched with user then it show its id
        if userdata is not None:
            login(req, userdata)
            # return render(req, "dashboard.html")
            return redirect("dashboard")
        else:
            context = {}
            context["errmsg"] = "Invalid email or password"
            return render(req, "signin.html", context)

def userlogout(req):
    logout(req)
    return redirect("/")

from django.core.mail import send_mail
from django.conf import settings
import random
from django.contrib import messages


def req_password(req):
    if req.method == "POST":
        uemail = req.POST["uemail"]
        try:
            user = User.objects.get(email=uemail)
            print(user.email, user)

            userotp = random.randint(1111, 999999)
            req.session["otp"] = userotp  # store otp into session

            subject = "PetStore- OTP for Reset Password"
            msg = f"Hello {user}\n Your OTP to reset password is:{userotp}\n Thank You for using our services."
            emailfrom = settings.EMAIL_HOST_USER
            receiver = [user.email]
            send_mail(subject, msg, emailfrom, receiver)

            return redirect("reset_password", uemail=user.email)

        except User.DoesNotExist:
            messages.error(req, "No account found with this email id.")
            return render(req, "req_password.html")
    else:
        return render(req, "req_password.html")


def reset_password(req, uemail):
    user = User.objects.get(email=uemail)
    print(user)
    if req.method == "POST":
        otp_entered = req.POST["otp"]
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        userotp = req.session.get("otp")
        print(userotp, type(userotp))
        print(otp_entered, type(otp_entered), upass, ucpass)

        if int(otp_entered) != int(userotp):
            messages.error(req, "OTP does not match! Try Again.")
            return render(req, "reset_password.html", {"uemail": uemail})

        elif upass != ucpass:
            messages.error(req, "Confirm password and password do not match.")
            return render(req, "reset_password.html", {"uemail": uemail})

        else:
            try:
                validate_password(upass)
                user.set_password(upass)
                user.save()
                return redirect("signin")
            except ValidationError as e:
                messages.error(req, str(e))
                return render(req, "reset_password.html", {"uemail": uemail})
    else:
        return render(req, "reset_password.html", {"uemail": uemail})


def about(req):
    return render(req,"about.html")

def contact(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        umobile = req.POST["umobile"]
        uemail = req.POST["uemail"]
        msg = req.POST["msg"]
        print(uname,umobile,uemail,msg)
        subject = "My Query"
        msg = f"Hello Team, {msg}"
        emailfrom = settings.EMAIL_HOST_USER
        receiver = [uemail]
        send_mail(subject, msg, emailfrom, receiver)
        
        return redirect("/")
    else:
        return render(req,"contact.html")