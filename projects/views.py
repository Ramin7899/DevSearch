# from crypt import methods
from multiprocessing import context
from turtle import title
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pkg_resources import require
from .models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .utils import searchProjects,paginateProjects
from django.contrib import messages



def projects(request):

    projects,search_query = searchProjects(request)

    custom_range,projects = paginateProjects(request,projects,3)

    contex = {'projects': projects,'search_query':search_query,'custom_range':custom_range}
    return render(request, 'projects/projects.html', contex)


def project(request, pk):
    projectobj = Project.objects.get(id=pk)

    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        reviw = form.save(commit=False)
        reviw.project = projectobj
        reviw.owner = request.user.profiles
        reviw.save()

        projectobj.getVoteCount

        messages.success(request,'Review Added')
        return redirect('project' , pk=projectobj.id)

    tags = projectobj.tags.all()
    return render(request, 'projects/single_project.html', {'project':projectobj , 'tags':tags,'form':form})

@login_required(login_url='login')
def createproject(request):
    profile = request.user.profiles
    form = ProjectForm()
    context = {'form':form}

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    return render(request,'projects/project_form.html', context)

@login_required(login_url='login')
def updateproject(request, pk):
    profile = request.user.profiles
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)
    context = {'form':form}

    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            form.save()
            return redirect('projects')

    return render(request,'projects/project_form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profiles
    project = profile.project_set.get(id=pk)
    context = {'object':project}

    if request.method == 'POST':
        project.delete()
        return redirect('projects')

    return render(request,'delete_template.html', context)

