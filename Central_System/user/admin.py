from django.contrib import admin

from .models import AccessRight, UserAccount, VehicleUsage, ElectricVehicle

admin.site.register(AccessRight)
admin.site.register(UserAccount)
admin.site.register(VehicleUsage)
admin.site.register(ElectricVehicle)

