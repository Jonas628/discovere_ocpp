from django.db import models
from django.utils import timezone
from datetime import date


#from .. cp_handler import enums
#from .. cp_handler import models as m
from ocpp_d.v16.enums import AuthorizationStatus

from enums import enums

"""
the foreign key must be part of the object B if relationship A - B = 1 : N
"""


class ChargingStation(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    position = models.TextField(null=True, blank=True)
    phase_rotation = models.CharField(max_length=3, choices=enums.PhaseRotation.choices,
                                      default=enums.PhaseRotation.RST)
    installation_date = models.DateTimeField()
    max_current = models.FloatField(max_length=6, default=16.0)
    # operating_status =

    def __str__(self):
        return "{0}".format(self.name)


# ChargePoint represents the communication domain
class ChargePoint(models.Model):
    charging_station = models.ForeignKey(to='ChargingStation', on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    slug = models.SlugField(unique=True)
    # ToDo add enums
    # registration_status = models.CharField(max_length=128)
    # availability_status = models.CharField(max_length=128)
    max_power = models.IntegerField(default=11000)
    protocol = models.CharField(max_length=10, choices=enums.BackendProtocol.choices,
                                default=enums.BackendProtocol.OCPP16_J)
    charge_point_model = models.CharField(max_length=128)
    charge_point_vendor = models.CharField(max_length=256)

    def __str__(self):
        return "{0}: {1}".format(self.charging_station.name, self.name)


class Connector(models.Model):
    charge_point = models.ForeignKey(to='ChargePoint', on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, default=0)
    socket_type = models.CharField(max_length=4, choices=enums.SocketType.choices,default=enums.SocketType.TYP2)
    max_current = models.FloatField(max_length=6, default=16.0)
    set_power_limit = models.IntegerField(default=11000)
    phase_rotation = models.CharField(max_length=3, choices=enums.PhaseRotation.choices,
                                      default=enums.PhaseRotation.RST)


class ChargePointConfiguration(models.Model):
    charge_point = models.ForeignKey(to='ChargePoint', on_delete=models.CASCADE)


class IdTag(models.Model):
    id_tag = models.CharField(max_length=20, default="0000000000000000")
    in_use = models.BooleanField(default=False)

    def __str__(self):
        return "{0}".format(self.id_tag)




class IdTagInfo(models.Model):
    id_tag = models.OneToOneField(IdTag, on_delete=models.CASCADE, primary_key=True)
    #type = models.
    expiry_date = models.DateTimeField()
    parent_id_tag = models.CharField(max_length=20, default="AAAAAAAAAAAAAAAA")
    status = models.CharField(max_length=32, choices=AuthorizationStatus.choices(),
                                      default=AuthorizationStatus.accepted)

    def is_active(self):
        if timezone.now() <= self.expiry_date:
            return True
        else:
            return False

    def to_json(self):
        json = {"expiry_date": str(self.expiry_date),
                  "parent_id_tag": str(self.parent_id_tag),
                  "status": self.status}
        return json


class Transaction(models.Model):
    charge_point_id = models.IntegerField(default=0)
    connector_id = models.IntegerField(default=0)
    start_id_tag = models.OneToOneField(IdTag, on_delete=models.CASCADE, null=True, related_name='start_id')
    stop_id_tag = models.OneToOneField(IdTag, on_delete=models.CASCADE, blank=True, related_name='stop_id')
    start_time = models.DateTimeField(null=True)
    stop_time = models.DateTimeField(null=True)
    start_meter_value = models.FloatField(blank=True)
    stop_meter_value = models.FloatField(blank=True)
    energy_consumed = models.FloatField(blank=True)