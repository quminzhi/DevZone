from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from base.models import Project, Tag

@api_view(['DELETE'])
def removeTag(request):
    tagID = request.data['tag']
    projectID = request.data['project']
    
    project = Project.objects.get(id=projectID)
    tag = Tag.objects.get(id=tagID)
    
    project.tags.remove(tag)
    
    return Response("Tag was deleted!")