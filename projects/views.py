# from crypt import methods
from multiprocessing import context
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pkg_resources import require
from .models import Project
from .forms import ProjectForm
from django.contrib.auth.decorators import login_required


def projects(request):
    projects = Project.objects.all()
    contex = {'projects': projects}
    return render(request, 'projects/projects.html', contex)


def project(request, pk):
    projectobj = Project.objects.get(id=pk)
    tags = projectobj.tags.all()
    return render(request, 'projects/single_project.html', {'projectobj':projectobj , 'tags':tags})

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
            return redirect('projects')

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

    return render(request,'projects/delete_template.html', context)

