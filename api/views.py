from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .serializer import ProjectSerializer
from projects.models import Project

from rest_framework.permissions import IsAuthenticated, IsAdminUser

from projects.models import Project, Module

# simple JSON Response
# def getRoutes(request):
#     routes = [
#         {"GET": '/api/projects'},
#         {"GET": '/api/projects/id'},

#         {"POST":'/api/users/token'},
#         {"POST": '/api/users/token/refresh'},
#     ]

#     return JsonResponse(routes, safe=False)


@api_view(["GET"])
def getRoutes(request):
    routes = [
        {"GET": '/api/projects'},
        {"GET": '/api/projects/id'},

        {"POST":'/api/users/token'},
        {"POST": '/api/users/token/refresh'},
    ]
    return Response(routes)


@api_view(["GET"])
def getProjects(request):
    print(f'Users: {request.user}')
    projects = Project.objects.all()
    serializer = ProjectSerializer(projects, many=True)

    return Response(serializer.data)



@api_view(["GET"])
@permission_classes([IsAuthenticated])
def getProject(request, pk):
    project = Project.objects.get(id=pk)
    serializer = ProjectSerializer(project, many=False)

    return Response(serializer.data)



@api_view(["DELETE"])
def removeModule(request):
    moduleId = request.data["module"]
    projectId = request.data['project']

    project =  Project.objects.get(id=projectId)
    module = Module.objects.get(id=moduleId)

    project.modules.remove(module)

    return Response(f"Module {module.name} removed.")

