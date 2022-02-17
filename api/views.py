from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from base.models import Project, Tag, Review
from .serializers import ProjectSerializer

from api import serializers


@api_view(['GET'])
def getRoutes(request):
    routes = [
        {'GET': '/api/projects/'},
        {'GET': '/api/project/id/'},

        {'POST': '/api/user/token/'},
        {'POST': '/api/user/token/refresh/'},

        {'POST': '/api/project/id/vote/'},

        {'DELETE': '/api/remove-tag/ (token required with \'api/user/token\', tag id and project id in JSON)'},
        {'PUT': '/api/add-tag/ (token required with \'api/user/token\', tag value and project id in JSON)'}
    ]

    return Response(routes)


@api_view(['GET'])
# @permission_classes([IsAuthenticated])
def getProjects(request):
    print('User:', request.user)
    projects = Project.objects.all()
    serializer = ProjectSerializer(
        projects, many=True)  # if only one, many=False
    return Response(serializer.data)


@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    serializer = ProjectSerializer(
        projects, many=False)  # if only one, many=False
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile  # pass along with token
    data = request.data  # JSON

    # print("DATA: ", data)
    
    # created is a flag, true if new record is created
    review, created = Review.objects.get_or_create(
        owner=user,
        project=project,
    )
    review.value = data['value']
    review.save()

    serializer = ProjectSerializer(project, many=False)
    return Response(serializer.data)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeTag(request):
    tagID = request.data['tag']
    projectID = request.data['project']

    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)

    project.tags.remove(tag)

    return Response("Tag was deleted!")

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def addTag(request):
    tag_value = request.data['tag']
    projectID = request.data['project']

    project = Project.objects.get(id=projectID)
    tag, created = Tag.objects.get_or_create(
        name=tag_value
    )
    project.tags.add(tag)

    return Response("Tag was added!")
