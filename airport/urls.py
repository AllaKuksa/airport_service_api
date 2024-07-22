from rest_framework import routers
from django.urls import path, include

from airport.views import (
    CrewViewSet,
    AirportViewSet,
    RouteViewSet,
)


router = routers.DefaultRouter()

router.register("crews", CrewViewSet)
router.register("airports", AirportViewSet)
router.register("routes", RouteViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "airport"
