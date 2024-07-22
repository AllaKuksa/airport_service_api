from django.shortcuts import render
from rest_framework import viewsets

from airport.models import Crew
from airport.serializers import CrewSerializer


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer

