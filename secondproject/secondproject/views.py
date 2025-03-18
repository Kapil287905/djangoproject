from django.shortcuts import HttpResponse

data=f"<hr><a href='/'>Home</a>\t<a href='/signup'>SignUP</a>\t<a href='/signin'>SignIN</a>"

def index(req):   
    return HttpResponse(f"<center><h1>Welcome my page{data}</h1></center>")

def signup(req):
    global username
    username = input("Enter username = ")
    return HttpResponse(f"<center><h1>SignUp page{data}</h1></center>")

def signin(req):
    checkusername = input("Enter username to signin = ")
    if checkusername == username:
        msgin=f"<center><h1>Welcome {checkusername}</h1></center>"
        logout=f"<hr><a href='/'>Logout</a><h1>"
        return HttpResponse(f"{msgin} {logout}")
    else:
        msg=f"<center><h1>Incorrect Username!! Try again</h1></center>"
        next=f"<hr><a href='/'>Click here to go Back</a><h1>"
        return HttpResponse(f"{msg}{next}")
    