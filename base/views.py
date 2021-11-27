from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .models import Project

# Create your views here.


def projects(request):
    projects = Project.objects.all()

    context = {
        'projects': projects,
    }

    return render(request, 'base/projects.html', context)


def singleProject(request, pk):
    project = Project.objects.get(id=pk)
    
    context = {
        'project': project,
    }

    return render(request, 'base/single-project.html', context)

@login_required(login_url='login')
def createProject(request):
    form = ProjectForm()
    
    if (request.method == 'POST'):
       form = ProjectForm(request.POST, request.FILES) # get image file
       if (form.is_valid):
           form.save()
           return redirect('projects')
            
    
    context = {
        'form': form,
    }
    
    return render(request, 'base/project-form.html', context)

@login_required(login_url='login')
def updateProject(request, pk):
    project = Project.objects.get(id=pk)
    form = ProjectForm(instance=project)
    
    if (request.method == 'POST'):
       form = ProjectForm(request.POST, request.FILES, instance=project)
       if (form.is_valid):
           form.save()
           return redirect('projects')
            
    
    context = {
        'form': form,
    }
    
    return render(request, 'base/project-form.html', context)

@login_required(login_url='login')
def deleteProject(request, pk):
    project = Project.objects.get(id=pk)
    
    if (request.method == 'POST'):
        project.delete()
        return redirect('projects')
    
    context = {
        'project': project,
    }
    
    return render(request, 'base/delete-template.html', context)