from .models import Skill, Profile
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

def paginateProfiles(request, profiles, items_per_page):
    page = request.GET.get('page')
    paginator = Paginator(profiles, items_per_page)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1  # set default page
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # last page
        profiles = paginator.page(page)

    half_range = 2
    leftIndex = int(page) - half_range
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + half_range + 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    
    
    return profiles, custom_range