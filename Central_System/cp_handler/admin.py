from django.contrib import admin

from .models import ChargePoint, ChargingStation, Connector, ChargePointConfiguration

admin.site.register(ChargePoint)
admin.site.register(ChargingStation)
admin.site.register(Connector)
admin.site.register(ChargePointConfiguration)
