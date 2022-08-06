from cmath import log
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profiles
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def profiles(request):
    profile = Profiles.objects.all()
    contex = {'profile':profile}
    return render(request, 'users/profiles.html', contex)

def userProfile(request, pk):
    profile = Profiles.objects.get(id=pk)

    top_skills = profile.skills_set.exclude(description__exact="")
    other_skills = profile.skills_set.filter(description__exact="")

    contex = {'profile':profile,'top_skills':top_skills,'other_skills':other_skills}
    return render(request, 'users/user-profile.html', contex)

def loginUser(request):

    page = 'login'

    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'username does not exist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, 'username inncorrect')

    contex = {'page':page}
    return render(request, 'users/login_register.html', contex)

def logoutUser(request):
    logout(request)
    messages.error(request, 'User was loggedout')
    return redirect('login')

def registerUser(request):
    form = UserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created!')

            login(request, user)
            return redirect('profiles')

        else:
            messages.success(request,'error')

    contex = {'page':page,'form':form}
    return render(request, 'users/login_register.html', contex)