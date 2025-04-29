from django.shortcuts import render, redirect,get_object_or_404
from .models import UserProfile, Products, Carts, Orders, Payments, Categories,Wishlist,Address
from django.contrib.auth.models import User

# Create your views here.


def index(req):
    allproducts = Products.objects.all()
    print(allproducts)
    allcategories = Categories.objects.all()
    print(allcategories)
    return render(
        req, "index.html", {"allproducts": allproducts, "allcategories": allcategories}
    )


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
            return redirect("/")
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
    return render(req, "about.html")


def contact(req):
    if req.method == "POST":
        uname = req.POST["uname"]
        umobile = req.POST["umobile"]
        uemail = req.POST["uemail"]
        msg = req.POST["msg"]
        print(uname, umobile, uemail, msg)

        subject = "My Query"
        msg = f"Hello Team, {msg}."
        emailfrom = settings.EMAIL_HOST_USER
        receiver = [uemail]
        send_mail(subject, msg, emailfrom, receiver)

        return redirect("/")
    else:
        return render(req, "contact.html")


from django.contrib import messages
from django.db.models import Q


def searchproduct(req):
    query=req.GET["q"]
    if query:
        allproducts=Products.objects.filter(
            Q(productname__icontains=query)
            |Q(description__icontains=query)
        )
        if len(allproducts)==0:
            messages.error(req,"No result found!!")
    else:
        allproducts=Products.objects.all()

    context={'allproducts':allproducts}
    return render(req, "index.html",context)

def electronics_search(req):
    if req.method=="GET":
        # ele_category=Categories.objects.filter(name="Electronics").first()
        # ele_category=Categories.objects.get(name="Electronics") # (=) for single row
        # print(ele_category)
        # allproducts = Products.objects.filter(categories=ele_category) # many row
        # print(allproducts)
        # context={'allproducts':allproducts}
        # if len(allproducts)==0:
        #     messages.error(req,"No result found!!")
        # return render(req, "index.html",context)

        allproducts=Products.Productmanager.electronics_list()
        print(allproducts)
        allcategories = Categories.objects.all()
        print(allcategories)
        context={'allproducts':allproducts, "allcategories": allcategories}
        if len(allproducts)==0:
            messages.error(req,"No result found!!")
        return render(req, "index.html",context)
    
def cloths_search(req):
    if req.method=="GET":
        allproducts=Products.Productmanager.cloths_list()
        print(allproducts)
        allcategories = Categories.objects.all()
        print(allcategories)
        context={'allproducts':allproducts, "allcategories": allcategories}
        if len(allproducts)==0:
            messages.error(req,"No result found!!")
        return render(req, "index.html",context)
    
def shoes_search(req):
    if req.method=="GET":
        allproducts=Products.Productmanager.shoes_list()
        print(allproducts)
        allcategories = Categories.objects.all()
        print(allcategories)
        context={'allproducts':allproducts, "allcategories": allcategories}
        if len(allproducts)==0:
            messages.error(req,"No result found!!")
        return render(req, "index.html",context)
    
def searchby_pricerange(req):
    if req.method == "GET":
        allcategories = Categories.objects.all()
        print(allcategories)
        context={"allcategories": allcategories}
        return render(req, "index.html",context)
    else:
        r1 = req.POST["min"]
        r2 = req.POST["max"]
        print(r1,r2)
        if r1 is not None and r2 is not None and r1.isdigit() and r2.isdigit():
            # allproducts = Products.objects.filter(price__range(r1,r2))
            allproducts = Products.Productmanager.pricerange(r1,r2)
            allcategories = Categories.objects.all()
            print(allcategories)
            context={'allproducts':allproducts, "allcategories": allcategories}
            if len(allproducts)==0:
                messages.error(req,"No result found!!")
            return render(req, "index.html",context)
        else:
            allproducts = Products.objects.all()
            allcategories = Categories.objects.all()
            context={'allproducts':allproducts, "allcategories": allcategories}
            return render(req, "index.html",context)
        
def sortingbyprice(req):
    sortoption=req.GET["sort"]
    if sortoption=="low_to_high":
        allproducts=Products.objects.order_by("price")
    elif sortoption=="high_to_low":
        allproducts=Products.objects.order_by("-price")
    else:
        allproducts = Products.objects.all()
    
    allcategories = Categories.objects.all()
    context={'allproducts':allproducts, "allcategories": allcategories}
    return render(req, "index.html",context)

def productdetail(req,productid):
    product=Products.objects.get(productid=productid)
    context={"product":product}
    return render(req, "productdetail.html",context)

def showwishlist(req):
    if req.user.is_authenticated:
        userid=req.user
        wishlist_item=Wishlist.objects.filter(userid=userid)
        context={"wishlist_item":wishlist_item}
        return render(req, "showwishlist.html", context)
    else:
        return redirect("signin")
    
def addtowishlist(req,productid):
    if req.user.is_authenticated:
        userid=req.user
        product = get_object_or_404(Products,productid=productid)
        if not Wishlist.objects.filter(userid=userid,productid=productid).exists():
            Wishlist.objects.create(userid=userid,productid=product)
            messages.success(req,'Product added to wishlist')
        else:
            messages.info(req,'Product already in wishlist')

        return redirect("showwishlist")
    else:
        return redirect("signin")

def deletetowishlist(req,productid):
    if req.user.is_authenticated:
        userid=req.user
        product = get_object_or_404(Products,productid=productid)
        wshlist_item=Wishlist.objects.filter(userid=userid, productid=product)
        wshlist_item.delete()
        messages.success(req, 'Product removed from wishlist')
        return redirect("showwishlist")
    else:
        messages.error(req,"You need to log in to add items to your wishlist")
        return redirect("signin")

from django.utils import timezone
from datetime import timedelta

def showcart(req):
    if req.user.is_authenticated:
        userid=req.user
        allcarts = Carts.objects.filter(userid=userid)

        totalitems=allcarts.count()
        # totalitems = sum(item.qty for item in allcarts)
        totalamount=sum(x.productid.price * x.qty for x in allcarts)

        has_profile=UserProfile.objects.filter(userid=userid).exists()
        has_address= Address.objects.filter(userid=userid).exists()

        estimated_delivery = timezone.now().date() + timedelta(days=5)

        context={"allcarts": allcarts,"userid":userid,"totalitems":totalitems,"totalamount":totalamount,"has_profile":has_profile,"has_address":has_address,"estimated_delivery":estimated_delivery}
        return render(req, "showcart.html", context)
    else:
        messages.error(req,"You need to log in to add items to your carts")
        return redirect("signin")
    
def updateqty(req,qv,productid):
    product = get_object_or_404(Products, productid=productid)
    allcarts = Carts.objects.filter(userid=req.user, productid=product)
    cart_item = allcarts.first()
    if qv==1:
        if cart_item.qty<product.quantity_available:
            cart_item.qty += 1
            cart_item.save()
        else:
            messages.error(req, 'Only limited stock available.')
    else:
        if cart_item.qty > 1:
            cart_item.qty -= 1
            cart_item.save()
        else:
            cart_item.delete()
    return redirect("showcart")

def deletetocart(req,productid):
    if req.user.is_authenticated:
        userid=req.user
        product = get_object_or_404(Products,productid=productid)
        cart_item=Carts.objects.filter(userid=userid, productid=product)
        cart_item.delete()
        messages.success(req, 'Product removed from cart')
        return redirect("showcart")
    else:
        messages.error(req,"You need to log in to add items to your cart")
        return redirect("signin")
    
def addtocart(req,productid):
    if req.user.is_authenticated:
        userid=req.user
        product = get_object_or_404(Products,productid=productid)
        cartitem,created=Carts.objects.get_or_create(userid=userid,productid=product)
        new_qty=cartitem.qty+1 if not created else 1
        if new_qty>product.quantity_available:
            messages.error(req,'cannot add mare itmes-only limited stock available')
            return redirect("showcart")
        
        cartitem.qty=new_qty
        cartitem.save()
        return redirect("showcart")

    else:
        messages.error(req,"You need to log in to add items to your carts")
        return redirect("signin")
    
from .forms import UserProfileForm,AddressForm
    
# def addprofile(req):
#     if req.method == "POST":
#         form=UserProfileForm(req.POST,req.FILES)
#         if form.is_valid():
#             profile=form.save(commit=False)
#             profile.userid=req.user
#             profile.save()
#             return redirect("showcart")
#     else:
#         form = UserProfileForm()
#     return render(req,'addprofile.html',{'form':form})
from datetime import datetime
def addprofile(req):
    user=req.user
    if not user.is_authenticated:
        return redirect("signin")
    
    if req.method=="POST":
        mobile=req.POST["mobile"]
        gender=req.POST["gender"]
        dob=req.POST["dob"]
        photo=req.FILES["photo"]

        if dob:
            dob_date=datetime.strptime(dob,"%Y-%m-%d").date()
            today=timezone.now().date()
            if dob_date>=today:
                messages.error(req,"Date of birth cannot be todays or future date")

            age=today.year-dob_date.year-((today.month,today.day)<(dob_date.month,dob_date.day)) 
            print(age)

            if age<18:
                messages.error(req,"Ypu must ne at least 18 years old to create profile")
                return render(req,'addprofile.html')
            
        UserProfile.objects.create(userid=user,mobile=mobile,gender=gender,dob=dob,photo=photo)
        return redirect("myprofile")
    else:
        return render(req,'addprofile.html')

def editprofile(req,profileid):
    profile=get_object_or_404(UserProfile,id=profileid)
    if req.method=="POST":
        profile.mobile=req.POST["mobile"]
        profile.gender=req.POST["gender"]
        profile.dob=req.POST["dob"]
        if req.FILES["photo"]:
            profile.photo=req.FILES["photo"]
        profile.save()
        return redirect('myprofile')
    return render(req,'editprofile.html',{'userprofile':profile})

def deleteprofile(req,profileid):
    profile=get_object_or_404(UserProfile,id=profileid)
    profile.delete()
    return redirect('myprofile')

def myprofile(req):
    user=req.user
    if not user.is_authenticated:
        return redirect("signin")
    
    userprofile=UserProfile.objects.filter(userid=user).first()
    address=Address.objects.filter(userid=user)
    context={"userid":user, "userprofile":userprofile,"address":address}
    return render(req,"myprofile.html",context)

# def addaddress(req):
#     if req.method == "POST":
#         form=AddressForm(req.POST)
#         if form.is_valid():
#             address=form.save(commit=False)
#             address.userid=req.user
#             address.save()
#             return redirect("showcart")
#     else:
#         form = AddressForm()
#     return render(req,'addaddress.html',{'form':form})

from .models import City,Country

def addaddress(req):
    user=req.user
    if not user.is_authenticated:
        return redirect("signin")
    
    if req.method=="POST":
         address=req.POST["address"]
         city=req.POST["city"]
         country=req.POST["country"]
         pincode=req.POST["pincode"]
         Address.objects.create(userid=user,address=address,city_id=city,country_id=country,pincode=pincode)
         return redirect('myprofile')
    
    cities=City.objects.all()
    countries=Country.objects.all()
    context={'cities':cities,'countries':countries}
    return render(req,'addaddress.html',context)

def deleteaddress(req,addressid):
    address=get_object_or_404(Address,id=addressid)
    address.delete()
    return redirect('myprofile')    

def editaddress(req,addressid):
    address=get_object_or_404(Address,id=addressid)
    if req.method=="POST":
        address.address=req.POST["address"]
        city_id=req.POST["city"]
        country_id=req.POST["country"]
        address.pincode=req.POST["pincode"]

        if city_id:
            address.city_id=city_id

        if country_id:
            address.city_id=country_id

        address.save()
        return redirect('myprofile')
    
    cities=City.objects.all()
    countries=Country.objects.all()
    context={'address':address,'cities':cities,'countries':countries}
    return render(req,'editaddress.html',context)