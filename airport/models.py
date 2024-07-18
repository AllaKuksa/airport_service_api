from django.db import models


class Crew(models.Model):
    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)

    class Meta:
        ordering = ("first_name",)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
