from rest_framework import viewsets, permissions
from events.models import Event
from core.models import Worker, Client
from .serializers import WorkerSerializer, ClientSerializer, EventSerializer
from .permissions import IsAuthorOrReadOnly


class WorkerViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Worker.objects.all()
    serializer_class = WorkerSerializer


class ClientViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAdminUser, )
    queryset = Client.objects.all()
    serializer_class = ClientSerializer


class EventViewSet(viewsets.ModelViewSet):
    permission_classes = (permissions.IsAuthenticated, IsAuthorOrReadOnly)
    queryset = Event.objects.all()
    serializer_class = EventSerializer
