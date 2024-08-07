from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError

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
from user.serializers import UserDetailSerializer


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name", "full_name")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_city = serializers.CharField(
        source="source.closest_big_city",
        read_only=True
    )
    destination_city = serializers.CharField(
        source="destination.closest_big_city"
    )

    class Meta:
        model = Route
        fields = (
            "id",
            "source_city",
            "destination_city",
            "distance"
        )


class RouteDetailSerializer(RouteSerializer):
    source = AirportSerializer(read_only=True, many=False)
    destination = AirportSerializer(read_only=True, many=False)

    class Meta:
        model = Route
        fields = (
            "id",
            "source",
            "destination",
            "distance",
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type_name = serializers.CharField(
        source="airplane_type.name",
        read_only=True
    )
    airplane_type = serializers.PrimaryKeyRelatedField(
        queryset=AirplaneType.objects.all(),
        write_only=True
    )

    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type_name",
            "airplane_type",
            "image",
            "capacity",
        )


class AirplaneImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = ("id", "image")


class FlightSerializer(serializers.ModelSerializer):
    departure_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    arrival_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "airplane",
            "crew",
            "departure_time",
            "arrival_time",
            "flight_duration_minutes",
        )


class FlightListSerializer(FlightSerializer):
    route_source = serializers.CharField(source="route.source", read_only=True)
    route_destination = serializers.CharField(
        source="route.destination",
        read_only=True
    )
    airplane = serializers.CharField(source="airplane.name", read_only=True)
    tickets_available = serializers.IntegerField(read_only=True)

    class Meta:
        model = Flight
        fields = (
            "id",
            "route_source",
            "route_destination",
            "departure_time",
            "arrival_time",
            "airplane",
            "tickets_available",
        )


class TicketSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        data = super(TicketSerializer, self).validate(attrs=attrs)
        Ticket.validate_ticket(
            attrs["row"],
            attrs["seat"],
            attrs["flight"].airplane,
            ValidationError,
        )
        return data

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class TicketListSerializer(TicketSerializer):
    flight = FlightListSerializer(read_only=True, many=False)

    class Meta:
        model = Ticket
        fields = ("id", "row", "seat", "flight", "order")


class OrderSerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M")
    tickets = TicketSerializer(
        many=True,
        required=False,
        allow_empty=True
    )

    class Meta:
        model = Order
        fields = (
            "id",
            "created_at",
            "tickets",
        )

    def create(self, validated_data):
        with transaction.atomic():
            tickets_data = validated_data.pop("tickets", [])
            order = Order.objects.create(**validated_data)
            for ticket_data in tickets_data:
                Ticket.objects.create(order=order, **ticket_data)
            return order


class OrderListSerializer(OrderSerializer):
    tickets = TicketListSerializer(many=True, read_only=True)


class TicketSeatsSerializer(TicketSerializer):
    class Meta:
        model = Ticket
        fields = ("row", "seat")


class FlightDetailSerializer(FlightSerializer):
    route = RouteDetailSerializer(read_only=True)
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )
    airplane = AirplaneSerializer(read_only=True, many=False)
    taken_places = TicketSeatsSerializer(
        source="tickets", many=True, read_only=True
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route",
            "departure_time",
            "arrival_time",
            "flight_duration_minutes",
            "airplane",
            "crew",
            "taken_places"
        )
