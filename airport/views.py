from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from django.db.models import F, Count

from airport.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Flight,
    Airplane,
    Order,
    Ticket
)
from airport.serializers import (
    CrewSerializer,
    AirportSerializer,
    RouteSerializer,
    RouteListSerializer,
    RouteDetailSerializer,
    AirplaneTypeSerializer,
    FlightSerializer,
    FlightListSerializer,
    FlightDetailSerializer,
    AirplaneSerializer,
    AirplaneImageSerializer,
    OrderSerializer,
    TicketSerializer,
    TicketListSerializer
)


class CrewViewSet(viewsets.ModelViewSet):
    queryset = Crew.objects.all()
    serializer_class = CrewSerializer


class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer

    def get_queryset(self):
        closest_big_city = self.request.query_params.get("closest_big_city")

        queryset = self.queryset

        if closest_big_city:
            queryset = queryset.filter(closest_big_city__icontains=closest_big_city)

        return queryset.distinct()


class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related(
        "source",
        "destination"
    )
    serializer_class = RouteSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return RouteListSerializer
        if self.action == "retrieve":
            return RouteDetailSerializer
        return RouteSerializer


class AirplaneTypeViewSet(viewsets.ModelViewSet):
    queryset = AirplaneType.objects.all()
    serializer_class = AirplaneTypeSerializer


class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related(
        "route",
        "airplane"
    ).prefetch_related(
        "crew"
    ).annotate(
        tickets_available=F(
            "airplane__rows"
        ) * F(
            "airplane__seats_in_row"
        ) - Count("tickets")
    )
    serializer_class = FlightSerializer

    def get_serializer_class(self):
        if self.action == "list":
            return FlightListSerializer
        if self.action == "retrieve":
            return FlightDetailSerializer
        return FlightSerializer


class AirplaneViewSet(viewsets.ModelViewSet):
    queryset = Airplane.objects.all().select_related(
        "airplane_type"
    )
    serializer_class = AirplaneSerializer

    def get_serializer_class(self):
        if self.action == "upload_image":
            return AirplaneImageSerializer
        else:
            return AirplaneSerializer

    @action(
        methods=["POST"],
        detail=True,
        permission_classes=[IsAdminUser],
        url_path="upload-image",
    )
    def upload_image(self, request, pk=None):
        airplane = self.get_object()
        serializer = self.get_serializer(airplane, data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related(
        "user"
    )
    serializer_class = OrderSerializer

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TickerViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all().select_related(
        "flight__route__source",
        "flight__route__destination",
        "flight__airplane"
    )
    serializer_class = TicketSerializer

    def get_serializer_class(self):
        if self.action in ("list", "retrieve"):
            return TicketListSerializer
        return TicketSerializer
