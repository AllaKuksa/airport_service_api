from django.contrib import admin

from airport.models import (
    Crew,
    Airport,
    Airplane,
    AirplaneType,
    Order,
    Route,
    Ticket,
    Flight
)


admin.site.register(Crew)
admin.site.register(Airplane)
admin.site.register(Airport)
admin.site.register(AirplaneType)
admin.site.register(Order)
admin.site.register(Route)
admin.site.register(Ticket)
admin.site.register(Flight)
