from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from .forms import MyUserCreationForm, ProfileForm, SkillForm, MessageForm
from django.contrib import messages
from .models import User
from .models import Profile, Message
from .utils import paginateProfiles, searchProfiles, account_activation_token

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
# Create your views here.

def loginView(request):
    page = 'login'

    if (request.user.is_authenticated):
        return redirect('profiles')

    if (request.method == 'POST'):
        email = request.POST['email'].lower()
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
        except:
            # messages is a key word in django, do not redefine it
            messages.error(request, "Husky email not found!")
            return redirect('login')

        if (not user.is_active):
            messages.warning(request, "Please activate your account first.")
            return redirect('login')
        else:
            user = authenticate(request, email=email, password=password)
            if (user is not None):
                login(request, user)
                return redirect(request.GET['back'] if 'back' in request.GET else 'account')
            else:
                messages.error(
                    request, "Husky email or password is not correct")
                return redirect('login')

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
        # delete inactivated user
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if (user is not None) and (user.is_active == False):
            user.delete()

        form = MyUserCreationForm(request.POST)
        if (form.is_valid()):
            user = form.save(commit=False)  # form return a user but not save

            # require for using uw email to signup
            if (not user.email.endswith('uw.edu')):
                messages.info(request, 'Please signup with UW email.')
                return redirect('register')

            user.username = user.username.lower()
            user.is_active = False  # wait for email confirmation
            user.save()

            current_site = get_current_site(request)
            subject = 'Activate Your Account@DevZone'
            message = render_to_string(
                'users/activation/email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }
            )
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(subject, message, to=[to_email])
            email.send()

            messages.info(
                request, 'User account was created but is waiting for activation.')
            return render(request, 'users/activation/activate.html')

        else:
            messages.error(request, 'An error occurred during registration')
            return redirect('register')

    context = {
        'page': page,
        'form': form,
    }

    return render(request, 'users/login-register.html', context)


def activateView(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.success(request, 'Welcome back ' + user.username + '!')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        messages.error(request, 'Sorry, we cannot verify your email')
        return HttpResponse('Activation link is invalid!')


def profiles(request):
    profiles, q = searchProfiles(request)
    profiles, custom_range = paginateProfiles(request, profiles, 3)

    context = {
        'profiles': profiles,
        'custom_range': custom_range,
        'q': q,
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
        if (form.is_valid()):
            form.save()
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'users/profile-form.html', context)


@login_required(login_url='login')
def createSkill(request):
    profile = request.user.profile
    form = SkillForm()

    if (request.method == 'POST'):
        form = SkillForm(request.POST)
        if (form.is_valid()):
            skill = form.save(commit=False)
            skill.owner = profile  # link to profile
            skill.save()
            messages.success(request, "Skill was added!")
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def updateSkill(request, pk):
    # TODO: find skills of request users
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill)

    if (request.method == 'POST'):
        form = SkillForm(request.POST, instance=skill)
        if (form.is_valid()):
            form.save()
            messages.success(request, "Skill was updated!")
            return redirect('account')

    context = {
        'form': form,
    }

    return render(request, 'users/skill-form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)

    if (request.method == 'POST'):
        skill.delete()
        messages.success(request, "Skill was deleted.")
        return redirect('account')

    context = {
        'object': skill,
    }

    return render(request, 'delete-template.html', context)


@login_required(login_url='login')
def inboxView(request):
    profile = request.user.profile
    # notice that messages here is the related name of recipient in model
    myMessages = profile.messages.all()
    unread_count = myMessages.filter(is_read=False).count()

    context = {
        'myMessages': myMessages,
        'unread_count': unread_count,
    }

    return render(request, 'users/inbox.html', context)


@login_required(login_url='login')
def messageView(request, pk):
    # pk: message id
    profile = request.user.profile
    # refer to Message with related name not default name message_set
    message = profile.messages.get(id=pk)
    if (message.is_read == False):
        message.is_read = True
        message.save()

    context = {
        'message': message,
    }

    return render(request, 'users/message.html', context)


def createMessage(request, pk):
    # pk: the profile id of recipient
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile  # login
    except:
        sender = None  # non-login

    if (request.method == 'POST'):
        form = MessageForm(request.POST)
        if (form.is_valid()):
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            # fill name and email for login user
            if (sender):
                message.name = sender.name
                message.email = sender.email
            message.save()
            messages.success(request, 'Message has been sent!')
            return redirect('user-profile', pk=recipient.id)

    context = {
        'recipient': recipient,
        'form': form,
    }

    return render(request, 'users/message-form.html', context)


@login_required(login_url='login')
def deleteMessage(request, pk):
    # pk: message id
    message = Message.objects.get(id=pk)
    message.delete()

    return redirect('inbox')