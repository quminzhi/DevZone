from django.shortcuts import redirect, render
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, ProfileForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import Profile

# Create your views here.


def loginView(request):
    page = 'login'

    if (request.user.is_authenticated):
        return redirect('profiles')

    if (request.method == 'POST'):
        username = request.POST['username']
        password = request.POST['password']

        try:
            user = User.objects.get(username=username)
        except:
            # messages is a key word in django, do not redefine it
            messages.error(request, "Username not found")

        user = authenticate(request, username=username, password=password)
        if (user is not None):
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "Username or password is not correct")

    context = {
        'page': page,
    }

    return render(request, 'users/login-register.html', context)


def logoutView(request):
    logout(request)
    messages.info(request, "Sayee again")
    return redirect('login')


def registerView(request):
    page = 'register'  # register and login share the same html
    form = MyUserCreationForm()

    if (request.method == 'POST'):
        form = MyUserCreationForm(request.POST)
        if (form.is_valid()):
            user = form.save(commit=False)  # form return a user but not save
            user.username = user.username.lower()
            user.save()

            messages.success(request, 'User account was created')
            login(request, user)
            return redirect('account')
        else:
            messages.error(request, 'An error occurred during registration')

    context = {
        'page': page,
        'form': form,
    }

    return render(request, 'users/login-register.html', context)


def profiles(request):
    profiles = Profile.objects.all()

    context = {
        'profiles': profiles,
    }

    return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    # get all skills with description
    top_skills = profile.skill_set.exclude(description__exact='')
    other_skills = profile.skill_set.filter(description='')

    context = {
        'profile': profile,
        'top_skills': top_skills,
        'other_skills': other_skills,
    }

    return render(request, 'users/user-profile.html', context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile

    # get all skills with description
    skills = profile.skill_set.all()
    projects = profile.project_set.all()

    context = {
        'profile': profile,
        'skills': skills,
        'projects': projects,
    }

    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def updateAccount(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if (request.method == 'POST'):
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if (form.is_valid):
            form.save()
            return redirect('account')
        
    context = {
        'form': form,
    }

    return render(request, 'users/profile-form.html', context)
