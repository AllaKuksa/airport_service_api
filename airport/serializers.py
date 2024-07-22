from rest_framework import serializers

from airport.models import (
    Crew,
    Airport,
    Route,
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
