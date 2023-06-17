from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.auth import authenticate, login

from .models import groupdatainfo, appliancesdatainfo
# purebase settings.......................................................................................................................
import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyD2xlH_N585bFljx1znka4PzArxv-JhovU",
  "authDomain": "home-auto1-dd018.firebaseapp.com",
  "databaseURL": "https://home-auto1-dd018-default-rtdb.firebaseio.com",
  "projectId": "home-auto1-dd018",
  "storageBucket": "home-auto1-dd018.appspot.com",
  "messagingSenderId": "258611597234",
  "appId": "1:258611597234:web:bfefc5e27439881a4f5eab",
  "measurementId": "G-WX0PEYBDCL"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
#..............................................................................................................................................



def index(request):
    return render(request, "signin.html")

def dashboard(request):
    context = {
        "groupdata":groupdatainfo.objects.filter(userg = request.user.username).all(),
        # "appliancedata":appliancesdatainfo.objects.filter(usera = request.user.username).all(),
    }
    return render(request, "dashboard.html", context)


def savegroup(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            groupname = request.POST.get('groupname')
            firegroupname = {groupname:''}
            print(request.user.username)
            if groupname != '':
                existing_models = groupdatainfo.objects.filter(userg = request.user.username, groupname = groupname)
                if len(existing_models) == 0:
                    your_model = groupdatainfo()
                    your_model.userg = request.user.username
                    your_model.groupname = groupname
                    your_model.save()
                    db.child(request.user.username).update(firegroupname)
                    messages.success(request, "Successfully created New Group")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Group already exists", extra_tags='danger')
                    return redirect('dashboard')
            else:
                messages.error(request, "Please enter a Group", extra_tags='danger')
                return redirect('dashboard')
        else:
            messages.error(request, "Please log in", extra_tags="danger")
            return redirect('index')
    return HttpResponse("failure")

def saveitem(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            itemname = request.POST.get('itemname')
            gname = request.POST.get('gname')
            fireitemname = {itemname:'OFF'}
            if gname != '' and itemname != '':
                existing_models = appliancesdatainfo.objects.filter(usera = request.user.username,appliancename = itemname, gpname = gname)
                if len(existing_models) == 0 :
                    your_model = appliancesdatainfo()
                    your_model.usera = request.user.username
                    your_model.appliancename = itemname
                    your_model.gpname = gname
                    your_model.status = 'OFF'
                    your_model.save()
                    db.child(request.user.username).child(gname).update(fireitemname)
                    messages.success(request, "Successfully created New Device")
                    return redirect('dashboard')
                else:
                    messages.error(request, "Device already exists", extra_tags='danger')
                    return redirect('dashboard')
            else:
                messages.error(request, "Please select a Group or enter a devicename", extra_tags='danger')
                return redirect('dashboard')
        else:
            messages.error(request, "Please log in", extra_tags="danger")
            return redirect('index')
    return HttpResponse("failure")



def listgroup(request, gpid):
    if request.user.is_authenticated:
        gpname = groupdatainfo.objects.get(id=gpid).groupname
        context = {
            "list":appliancesdatainfo.objects.filter(gpname = gpname, usera = request.user.username).all(),
            "groupdata":groupdatainfo.objects.filter(userg = request.user.username).all(),
            "gpname":gpname,
        }
        return render(request,'dashboard.html', context)
    else:
        return HttpResponse("eroorr")
    


def deletegroup(request, gpid):
    if request.user.is_authenticated:
        gpobj = groupdatainfo.objects.get(id=gpid)
        gpname = groupdatainfo.objects.get(id=gpid).groupname
        applianceobj = appliancesdatainfo.objects.filter(gpname = gpname, usera = request.user.username)
        gpobj.delete()
        applianceobj.delete()
        db.child(request.user.username).child(gpname).remove()
        return redirect('dashboard')
    else:
        return HttpResponse("error in deletion")


def deleteitem(request, gpid):
    if request.user.is_authenticated:
        gpobj = appliancesdatainfo.objects.get(id=gpid)
        firegroupname = gpobj.gpname
        fireitemname = gpobj.appliancename
        gpobj.delete()
        db.child(request.user.username).child(firegroupname).child(fireitemname).remove()
        return redirect('dashboard')
    else:
        return HttpResponse("error in deletion")
    

def changestatus(request, gpid):
    if request.user.is_authenticated:
        gpobj = appliancesdatainfo.objects.get(id=gpid)
        firegroupname = gpobj.gpname
        
        if gpobj.status == 'OFF':
            gpobj.status = 'ON'
            fireitemname = {gpobj.appliancename:"ON"}
            db.child(request.user.username).child(firegroupname).update(fireitemname)
        else:
            gpobj.status = 'OFF'
            fireitemname = {gpobj.appliancename:"OFF"}
            db.child(request.user.username).child(firegroupname).update(fireitemname)
        gpobj.save()    
        return redirect('dashboard')
    else:
        return HttpResponse("Error in changing status")


def signup(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        if User.objects.filter(username = username):
            messages.error(request, "Username already exists", extra_tags="danger")
            return redirect('index')
        elif User.objects.filter(email=email):
            messages.error(request, "Email already exists", extra_tags="danger")
            return redirect('index')
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Successfully created account, Enjoy")
            return redirect('dashboard')
    return HttpResponse("signup failed")



def signin(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged in")
            return redirect('dashboard')
        else:
            messages.error(request, "No user found with the credentials provided", extra_tags="danger")
            return redirect('index')


def changepassword(request):
    if request.user.is_authenticated:
        newpass = request.POST.get("newpass")
        user = User.objects.get(username = request.user.username)
        user.set_password(newpass)
        user.save()
        messages.success(request, 'Successfully changed Password. Please Signin again')
        return redirect('index')
    else:
        messages.error(request, "Error in Password change", extra_tags='danger')
        return redirect('dashboard')


def logout_view(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('index')