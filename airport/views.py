from drf_spectacular.types import OpenApiTypes
from drf_spectacular.utils import extend_schema, OpenApiParameter
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
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
            queryset = queryset.filter(
                closest_big_city__icontains=closest_big_city
            )

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="closest_big_city",
                type=OpenApiTypes.STR,
                description="Filter by closest_big_city"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
        "airplane",
        "route__source",
        "route__destination"
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

    def get_queryset(self):
        departure_time = self.request.query_params.get("departure_time")
        source = self.request.query_params.get("route_source")
        destination = self.request.query_params.get("route_destination")

        queryset = self.queryset

        if departure_time:
            queryset = queryset.filter(
                departure_time__icontains=departure_time
            )
        if source:
            queryset = queryset.filter(
                route__source__closest_big_city__icontains=source
            )
        if destination:
            queryset = queryset.filter(
                route__destination__closest_big_city__icontains=destination
            )

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="departure_time",
                type=OpenApiTypes.DATE,
                description="Filter by departure time"
            ),
            OpenApiParameter(
                name="route_source",
                type=OpenApiTypes.STR,
                description="Filter by route source"
            ),
            OpenApiParameter(
                name="route_destination",
                type=OpenApiTypes.STR,
                description="Filter by route destination"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)


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
    permission_classes = (IsAuthenticated,)

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

    def get_queryset(self):
        order_id_str = self.request.query_params.get("order")
        queryset = self.queryset

        if order_id_str:
            queryset = queryset.filter(order_id=int(order_id_str))

        return queryset.distinct()

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name="order",
                type=OpenApiTypes.INT,
                description="Filter by order id (ex. ?order=2)"
            )
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
