from rest_framework import viewsets, permissions
from rest_framework.response import Response
from .models import Client, Project
from .serializers import ClientSerializer, ProjectSerializer

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]  # Require authentication to access

    def list(self, request, *args, **kwargs):
        user_projects = Project.objects.filter(users=request.user)
        serializer = self.get_serializer(user_projects, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        # Add logged-in user to the project's users when creating a project
        request.data['users'] = [request.user.id]
        return super().create(request, *args, **kwargs)
