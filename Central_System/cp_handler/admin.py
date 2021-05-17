from django.contrib import admin

from cp_handler.models.models import ChargePoint, ChargingStation, Connector, ChargePointConfiguration, IdTag, \
    IdTagInfo, Transaction
from user.models import Address

admin.site.register(ChargePoint)
admin.site.register(ChargingStation)
admin.site.register(Connector)
admin.site.register(ChargePointConfiguration)
admin.site.register(IdTag)
admin.site.register(IdTagInfo)
admin.site.register(Address)
admin.site.register(Transaction)
