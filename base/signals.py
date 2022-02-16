from .models import Profile, Review

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# signal method 1:
@receiver(post_save, sender=Review)
def alert(sender, instance, created, **kwargs):
    project = sender.project
    project.refreshVoteCount