from django.shortcuts import HttpResponse

def index(req):
    return HttpResponse("Session-Server side and Cookies-client side")

def setsession(req):
    req.session['username']='komal'
    req.session['password']='1234565'
    return HttpResponse('Session are set')

def getsession(req):
    username=req.session["username"]
    password=req.session["password"]
    # req.session.flush()
    return HttpResponse("username = "+username+" password = "+password)
    
def setcookies(req):
    response=HttpResponse("Cookies are ser")
    response.set_cookie("admin","123456789")
    response.set_cookie("username","admin")
    response.set_cookie("password","123456789")
    return response

def getcookies(req):
    data=req.COOKIES['admin']
    username=req.COOKIES['username']
    password=req.COOKIES['password']
    return HttpResponse(data+" "+username+" "+password)