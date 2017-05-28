from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import views, viewsets, generics, parsers, response
import django_filters
from django_filters import rest_framework as filters
from .models import Task, Event, Play, LogFile
from .serializers import UserSerializer, GroupSerializer, \
                         TaskSerializer, EventSerializer, \
                         PlaySerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer


class EventFilter(filters.FilterSet):

    event_name = django_filters.CharFilter(name="name",
                                           label="name",
                                           lookup_expr=["exact", "iexact", "contains"])
    hostname = django_filters.CharFilter(name="data__host",
                                         label="hostname")

    data = django_filters.CharFilter(name="data",
                                     label="data",
                                     lookup_expr=["contains", "contained_by"])

    after = django_filters.DateTimeFilter(name="created",
                                          label="after",
                                          lookup_expr=["gte"])
    before = django_filters.DateTimeFilter(name="created",
                                           label="before",
                                           lookup_expr=["lte"])

    class Meta:
        model = Event
        fields = (
            "name",
            "hostname",
            "data",
            "after",
            "before",
        )


class EventViewSet(viewsets.ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()
    filter_backends = (filters.DjangoFilterBackend,)
    filter_class = EventFilter


class PlayViewSet(viewsets.ModelViewSet):
    queryset = Play.objects.all()
    serializer_class = PlaySerializer


class FileUploadView(views.APIView):
    parser_classes = (parsers.FileUploadParser,)

    def put(self, request, filename, format=None):
        file_obj = request.data["file"]
        lf = LogFile(log_file=file_obj)
        lf.save()
        return response.Response(status=204)
