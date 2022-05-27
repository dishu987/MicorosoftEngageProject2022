from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login,logout, authenticate
from django.contrib import messages
# Create your views here.
def register(response):
    logout(response)
    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            messages.success(response,'Congratutaions! Now you are eligible for admin panel.')
        else:
            messages.error(response,'Error! you make mistake to fill form.')
    else:
        form = UserCreationForm()
    form = UserCreationForm()
    if response.user.is_anonymous:
        context = {"message": "You are not logged in"}
        context["form"]=form
        context["entry"] = ""
        context["nav1"] = "Student Login"
        context["link1"] = "login"
        context["nav2"] = "Sign Up"
        context["link2"] = "loginProf"
    else:
        context = {"message": f"You are logged in as {response.user.username}"}
        context["entry"] = response.user.username
        context["form"]=form
        context["nav2"] = f"Logout ({response.user.username})"
        context["link2"] = "logout"
    return render(response,"register/register.html",context)
