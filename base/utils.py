from .models import Tag, Project
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def searchProjects(request):
    q = ''
    if (request.GET.get('q')):
        q = request.GET.get('q')
    
    tags = Tag.objects.filter(name__icontains=q)
    
    projects = Project.objects.distinct().filter(
        Q(title__icontains=q) |
        Q(description__icontains=q) |
        Q(owner__name__icontains=q) |
        Q(tags__in=tags)
    )
    
    return projects, q

def paginateProjects(request, projects, items_per_page):
    page = request.GET.get('page')
    paginator = Paginator(projects, items_per_page)

    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1  # set default page
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages  # last page
        projects = paginator.page(page)

    half_range = 2
    leftIndex = int(page) - half_range
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = int(page) + half_range + 1
    if rightIndex > paginator.num_pages:
        rightIndex = paginator.num_pages + 1
    
    custom_range = range(leftIndex, rightIndex)
    
    
    return projects, custom_range