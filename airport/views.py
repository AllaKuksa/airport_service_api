from rest_framework import viewsets

from airport.models import (
    Crew,
    Airport
)
from airport.serializers import (
    CrewSerializer,
    AirportSerializer
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
