from rest_framework import routers
from django.urls import path, include

from airport.views import (
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
    AirplaneTypeViewSet,
    FlightViewSet,
    AirplaneViewSet,
)


router = routers.DefaultRouter()

router.register("crews", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("flights", FlightViewSet)
router.register("airplanes", AirplaneViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
