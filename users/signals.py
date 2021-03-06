from .models import User
from .models import Profile

from django.db.models.signals import post_save, post_delete
# from django.dispatch import receiver

from django.core.mail import send_mail
from django.conf import settings

# # signal method 1:
# @receiver(post_save, sender=Profile)
# def alert(sender, instance, created, **kwargs):
#     print("sender: ", sender) # sender:  <class 'users.models.Profile'>
#     print("instance: ", instance) # instance:  minzhi
#     print("created: ", created) # created:  False


# signal method 2: create profile if user is created
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        subject = 'Welcome to UW DevZone'
        message = 'We are glad you are here.'
                
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False,
        )

# if profile is update then update responding items in user
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )


# if profile is update then update responding items in user
def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if (created == False):
        # profile.name actually refers to the first name of the user
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()


# if profile is deleted then user is deleted
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        user.delete()
    except:
        pass


post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)
post_delete.connect(deleteUser, sender=Profile)
