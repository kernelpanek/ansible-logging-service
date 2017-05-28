from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import Task, Event, Play, LogFile
import logging

logger = logging.getLogger(__name__)


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ("url", "username", "email", "groups")


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ("url", "name")


class TaskSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Task
        fields = ("id", "name", "data", "created", "hostip", "hostname", "user")


class EventSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Event
        fields = ("id", "name", "data", "created", "hostip", "hostname", "user")


class PlaySerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Play
        fields = ("id", "name", "data", "created", "hostip", "hostname", "user")
