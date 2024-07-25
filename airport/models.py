import os
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify
from django.conf import settings
from rest_framework.exceptions import ValidationError


class Crew(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        ordering = ("first_name",)

    def __str__(self):
        return f"{self.full_name}"


class Airport(models.Model):
    name = models.CharField(max_length=255)
    closest_big_city = models.CharField(max_length=255)

    class Meta:
        ordering = ("closest_big_city",)

    def __str__(self):
        return f"{self.closest_big_city}: airport {self.name}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_as_source"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes_as_destination"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        ordering = ("source", "destination", "distance")

    def __str__(self):
        return (f"{self.source.closest_big_city} - "
                f"{self.destination.closest_big_city} - {self.distance} km")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.name)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/airplanes/", filename)


class Airplane(models.Model):
    name = models.CharField(max_length=255)
    rows = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(60),
        ]
    )
    seats_in_row = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ]
    )
    airplane_type = models.ForeignKey(
        AirplaneType,
        on_delete=models.CASCADE,
        related_name="airplanes",
    )
    image = models.ImageField(null=True, upload_to=movie_image_file_path)

    @property
    def capacity(self) -> int:
        return self.rows * self.seats_in_row

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return (f"{self.name} - type {self.airplane_type.name},  "
                f"number of seats: {self.capacity}")


class Flight(models.Model):
    route = models.ForeignKey(
        Route,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    airplane = models.ForeignKey(
        Airplane,
        on_delete=models.CASCADE,
        related_name="flights",
    )
    crew = models.ManyToManyField(Crew)
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()

    @property
    def flight_duration_minutes(self) -> int:
        return int((self.arrival_time - self.departure_time).total_seconds() / 60)

    class Meta:
        ordering = ("route", )
        unique_together = (
            "route",
            "airplane",
            "departure_time",
            "arrival_time"
        )

    def __str__(self):
        return f"{self.route}: {self.departure_time} - {self.arrival_time}"


class Order(models.Model):
    created_at = models.DateTimeField()
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders",
    )

    class Meta:
        ordering = ("created_at", )

    def __str__(self):
        return f"{self.created_at} - {self.user}"


class Ticket(models.Model):
    row = models.PositiveIntegerField()
    seat = models.PositiveIntegerField()
    flight = models.ForeignKey(
        Flight,
        on_delete=models.CASCADE,
        related_name="tickets"
    )
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "flight")
        ordering = ("flight", "row", "seat")

    @staticmethod
    def validate_ticket(row, seat, airplane, error_to_raise):
        for ticket_attr_value, ticket_attr_name, airplane_attr_name in [
            (row, "row", "rows"),
            (seat, "seat", "seats_in_row"),
        ]:
            count_attrs = getattr(airplane, airplane_attr_name)
            if not (1 <= ticket_attr_value <= count_attrs):
                raise error_to_raise(
                    {
                        ticket_attr_name: f"{ticket_attr_name} "
                                          f"number must be in available range: "
                                          f"(1, {airplane_attr_name}): (1, {count_attrs})"
                    }
                )

    def clean(self):
        Ticket.validate_ticket(
            self.row,
            self.seat,
            self.flight.airplane,
            ValidationError,
        )

    def save(
            self,
            force_insert=False,
            force_update=False,
            using=None,
            update_fields=None
    ):
        self.full_clean()
        return super(Ticket, self).save(
            force_insert, force_update, using, update_fields
        )

    def __str__(self):
        return f"{self.flight}  (row: {self.row}, seat: {self.seat})"
