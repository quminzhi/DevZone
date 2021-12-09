from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Project, Tag, Review
from .serializers import ProjectSerializer
from base.models import Project

from api import serializers

@api_view(['DELETE'])
def removeTag(request):
    tagID = request.data['tag']
    projectID = request.data['project']
    
    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)
    
    project.tags.remove(tag)
    
    return Response("Tag was deleted!")

@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},
        
        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'},
    ]
    
    return Response(routes)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getProjects(request):
    print('User:', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True) # if only one, many=False
    return Response(serializer.data)

@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(projects, many=False) # if only one, many=False
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile # pass along with token
    data = request.data
    
    # print("DATA: ", data)
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    review.value = data['value']
    review.save()
    project.refreshVoteCount
        
    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)