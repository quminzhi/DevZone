from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import ProjectForm
from .models import Project
from .utils import searchProjects, paginateProjects



def projects(request):
    projects, q = searchProjects(request)
    projects, custom_range = paginateProjects(request, projects, 3)
    
    context = {
        'custom_range': custom_range,
        'projects': projects,
        'q': q,
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
    profile = request.user.profile
    form = ProjectForm()

    if (request.method == 'POST'):
        form = ProjectForm(request.POST, request.FILES)  # get image file
        if (form.is_valid):
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'base/project-form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if (request.method == 'POST'):
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if (form.is_valid):
            form.save()
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'base/project-form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if (request.method == 'POST'):
        project.delete()
        return redirect('account')

    context = {
        'object': project,
    }

    return render(request, 'delete-template.html', context)
