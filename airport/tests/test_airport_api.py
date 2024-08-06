from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils.timezone import make_aware
from rest_framework import status
from rest_framework.test import APIClient
from django.urls import reverse
from datetime import datetime

from airport.models import (
    Airport,
    Route,
    AirplaneType,
    Airplane, Crew, Flight
)
from airport.serializers import FlightListSerializer, FlightDetailSerializer

FLIGHT_URL = reverse("airport:flight-list")


def detail_url(flight_id):
    return reverse("airport:flight-detail", args=[flight_id])


def sample_airport(**params):
    defaults = {
        "name": "Test Airport",
        "closest_big_city": "Test City",
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "distance": 100,
        "source": sample_airport(),
        "destination": sample_airport(),
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "Test Airplane Type",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "Test Airplane",
        "rows": 5,
        "seats_in_row": 8,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_crew(**params):
    defaults = {
        "first_name": "Test Crew First Name",
        "last_name": "Test Crew Last Name",
    }
    defaults.update(params)
    return Crew.objects.create(**defaults)


def sample_flight(**params):
    defaults = {
        "departure_time": make_aware(datetime(2024, 12, 10, 11, 0)),
        "arrival_time": make_aware(datetime(2024, 12, 10, 19, 0)),
        "route": sample_route(),
        "airplane": sample_airplane(),
    }
    defaults.update(params)
    flight = Flight.objects.create(**defaults)
    crew1 = sample_crew()
    crew2 = sample_crew(first_name="Another", last_name="Crew Member")
    flight.crew.add(crew1, crew2)
    return flight


class UnauthorizedFlightAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        response = self.client.get(FLIGHT_URL)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthorizedFlightAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test.com",
            password="<PASSWORD>",
            passport_number="123456",
            date_of_birth="1990-12-13"
        )
        self.client.force_authenticate(user=self.user)

    def test_flights_list(self):
        sample_flight()
        sample_flight()
        response = self.client.get(FLIGHT_URL)

        flights = Flight.objects.all()

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_flights_with_departure_time_filter(self):
        flight_1 = sample_flight(departure_time="2024-10-10 11:00")
        flight_2 = sample_flight(departure_time="2024-01-10 11:00")
        response = self.client.get(
            FLIGHT_URL,
            {"departure_time": "2024-10-10 11:00"}
        )

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        serializer_1 = FlightListSerializer(flight_1)
        serializer_2 = FlightListSerializer(flight_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_1.data, response.data["results"])
        self.assertNotIn(serializer_2.data, response.data["results"])

    def test_flights_with_route_source_filter(self):
        flight_1 = sample_flight()
        flight_2 = sample_flight()

        response = self.client.get(FLIGHT_URL, {"route_source": "Test"})

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        serializer_1 = FlightListSerializer(flight_1)
        serializer_2 = FlightListSerializer(flight_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(serializer_1.data, response.data["results"])
        self.assertIn(serializer_2.data, response.data["results"])
        self.assertEqual(2, len(response.data["results"]))

    def test_flights_with_route_destination_filter(self):
        airport = sample_airport(closest_big_city="Another City")
        sample_route_2 = sample_route(destination=airport)
        flight_1 = sample_flight()
        flight_2 = sample_flight(route=sample_route_2)

        response = self.client.get(
            FLIGHT_URL,
            {"route_destination": "Another"}
        )

        for flight in response.data["results"]:
            flight.pop("tickets_available", None)

        serializer_1 = FlightListSerializer(flight_1)
        serializer_2 = FlightListSerializer(flight_2)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertNotIn(serializer_1.data, response.data["results"])
        self.assertIn(serializer_2.data, response.data["results"])

    def test_retrieve_flight_detail(self):
        flight = sample_flight()
        url = detail_url(flight.id)

        response = self.client.get(url)
        serializer = FlightDetailSerializer(flight)

        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_creat_flight_forbidden(self):
        payload = {
            "departure_time": make_aware(datetime(2025, 12, 10, 11, 0)),
            "arrival_time": make_aware(datetime(2025, 12, 10, 19, 0)),
        }
        response = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
