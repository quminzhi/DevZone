from .models import Skill, Profile
from django.db.models import Q

def searchProfiles(request):
    q = ''
    if (request.GET.get('q')):
        q = request.GET.get('q')
    
    skills = Skill.objects.filter(name__icontains=q)
    
    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=q) |
        Q(short_intro__icontains=q) |
        Q(skill__in=skills)
    )
    
    return profiles, q