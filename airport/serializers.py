from rest_framework import serializers

from airport.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Flight, Airplane,
)


class CrewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Crew
        fields = ("id", "first_name", "last_name")


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ("id", "name", "closest_big_city")


class RouteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Route
        fields = ("id", "source", "destination", "distance")


class RouteListSerializer(RouteSerializer):
    source_city = serializers.CharField(source="source.closest_big_city")
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


class RouteDetailSerializer(RouteListSerializer):
    source_airport = serializers.CharField(source="source.name")
    destination_airport = serializers.CharField(source="destination.name")

    class Meta:
        model = Route
        fields = (
            "id",
            "source_city",
            "source_airport",
            "destination_city",
            "destination_airport",
            "distance"
        )


class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ("id", "name")


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
    route_source = serializers.CharField(source="route.source")
    route_destination = serializers.CharField(source="route.destination")
    airplane = serializers.CharField(source="airplane.name")
    crew = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field="full_name"
    )

    class Meta:
        model = Flight
        fields = (
            "id",
            "route_source",
            "route_destination",
            "departure_time",
            "arrival_time",
            "airplane",
            "crew"
        )


class FlightDetailSerializer(FlightListSerializer):
    distance = serializers.IntegerField(source="route.distance")
    number_of_seats = serializers.IntegerField(source="airplane.capacity")

    class Meta:
        model = Flight
        fields = (
            "id",
            "route_source",
            "route_destination",
            "departure_time",
            "arrival_time",
            "flight_duration_minutes",
            "distance",
            "airplane",
            "number_of_seats",
            "crew"
        )


class AirplaneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airplane
        fields = (
            "id",
            "name",
            "rows",
            "seats_in_row",
            "airplane_type",
            "image",
            "capacity",
        )
