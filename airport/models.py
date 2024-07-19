import os
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils.text import slugify


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
        return f"{self.closest_big_city} - airport {self.name}"


class Route(models.Model):
    source = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    destination = models.ForeignKey(
        Airport,
        on_delete=models.CASCADE,
        related_name="routes"
    )
    distance = models.PositiveIntegerField()

    class Meta:
        ordering = ("source", "destination", "distance")

    def __str__(self):
        return (f"Distance from {self.source.name} - {self.destination.name}"
                f" is {self.distance} km")


class AirplaneType(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ("name",)

    def __str__(self):
        return self.name


def movie_image_file_path(instance, filename):
    _, extension = os.path.splitext(filename)
    filename = f"{slugify(instance.title)}-{uuid.uuid4()}{extension}"

    return os.path.join("uploads/movies/", filename)


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
        return (f"{self.name} - type {self.airplane_type.name} "
                f"has {self.capacity} seats")


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

    class Meta:
        ordering = ("route", )
        unique_together = ("route", "airplane", "departure_time", "arrival_time")

    def __str__(self):
        return f"{self.route}: {self.departure_time} - {self.arrival_time}"