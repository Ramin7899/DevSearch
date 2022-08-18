from cmath import log
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import Profiles, Skills
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileForm, SkillForm
from .utils import searchProfiles,paginateProfiles
# Create your views here.

def profiles(request):


    profiles, search_query = searchProfiles(request)

    custom_range,profiles = paginateProfiles(request,profiles,3)

    contex = {'profile':profiles,'search_query':search_query,'custom_range':custom_range}
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
    messages.info(request, 'User was loggedout')
    return redirect('login')

def registerUser(request):
    form = CustomUserCreationForm()
    page = 'register'

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            print("here")
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()

            messages.success(request,'User account was created!')

            login(request, user)
            return redirect('edit-account')

        else:
            messages.success(request,'error')
            

    contex = {'page':page,'form':form}
    return render(request, 'users/login_register.html', contex)


@login_required(login_url='login')
def userAccount(request):

    profile = request.user.profiles
    skills = profile.skills_set.all()
    projects = profile.project_set.all()

    contex = {'profile':profile,'skills':skills,'projects':projects}
    return render(request, 'users/account.html', contex)

@login_required(login_url='login')
def editAccount(request):
    
    profile = request.user.profiles
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('account')

    contex = {'form':form}
    return render(request, 'users/profile_form.html', contex)

@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profiles
    form = SkillForm()


    if request.method =='POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was added successfully!')
            return redirect('account')


    contex = {'form':form}
    return render(request, 'users/skill_form.html', contex)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile = request.user.profiles
    skill = profile.skills_set.get(id=pk)
    form = SkillForm(instance=skill)


    if request.method =='POST':
        form = SkillForm(request.POST,instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully!')
            return redirect('account')


    contex = {'form':form}
    return render(request, 'users/skill_form.html', contex)

def deleteSkill(request, pk):

    profile = request.user.profiles
    skill = profile.skills_set.get(id=pk)

    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'Skill was delete successfully!')
        return redirect('account')

    contex = {'object':skill}
    return render(request, 'delete_template.html', contex)
