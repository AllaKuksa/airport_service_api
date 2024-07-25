from rest_framework import serializers

from airport.models import (
    Crew,
    Airport,
    Route,
    AirplaneType,
    Flight, Airplane, Order,
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
    source_city = serializers.CharField(source="source.closest_big_city", read_only=True)
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
    source_airport = serializers.CharField(source="source.name", read_only=True)
    destination_airport = serializers.CharField(source="destination.name", read_only=True)

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
    route_source = serializers.CharField(source="route.source", read_only=True)
    route_destination = serializers.CharField(source="route.destination", read_only=True)
    airplane = serializers.CharField(source="airplane.name", read_only=True)
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
    distance = serializers.IntegerField(source="route.distance", read_only=True)
    number_of_seats = serializers.IntegerField(source="airplane.capacity", read_only=True)

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
    airplane_type_name = serializers.CharField(source="airplane_type.name", read_only=True)
    airplane_type = serializers.PrimaryKeyRelatedField(queryset=AirplaneType.objects.all(), write_only=True)

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


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ("id","created_at", "user")