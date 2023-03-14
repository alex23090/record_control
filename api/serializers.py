from core.models import Worker, Client
from events.models import Event
from rest_framework import serializers


class WorkerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Worker
        fields = ('user', 'name', 'username', 'email', 'bio', 'created')


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('user', 'name', 'username', 'email', 'created')


class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = ('id', 'client', 'worker', 'date', 'start_time', 'end_time', 'approved')
