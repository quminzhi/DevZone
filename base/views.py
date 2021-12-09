from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProjectForm, ReviewForm
from .models import Project, Tag
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
    form = ReviewForm()

    if (request.method == 'POST'):
        form = ReviewForm(request.POST)
        review = form.save(commit=False)
        review.project = project
        review.owner = request.user.profile
        review.save()
        messages.success(request, 'Thanks for your review!')
        
        project.refreshVoteCount
        
        return redirect('single-project', pk=project.id)
    
    context = {
        'project': project,
        'form': form,
    }

    return render(request, 'base/single-project.html', context)


@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if (request.method == 'POST'):
        newTags = request.POST.get('new-tags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES)  # get image file
        if (form.is_valid):
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
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
        newTags = request.POST.get('new-tags').replace(',', ' ').split()
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if (form.is_valid):
            project = form.save()
            for tag in newTags:
                tag, created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
                
            return redirect('account')

    context = {
        'form': form,
        'project': project,
    }

    return render(request, 'base/project-form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if (request.method == 'POST'):
        project.delete()
        return redirect(request.GET['back'] if 'back' in request.GET else 'account')

    context = {
        'object': project,
    }

    return render(request, 'delete-template.html', context)
