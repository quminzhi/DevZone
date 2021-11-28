from .models import Tag, Project
from django.db.models import Q

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