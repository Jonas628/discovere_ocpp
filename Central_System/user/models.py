from django.db import models
import Central_System
from datetime import datetime, date


#from .. cp_handler import enums
#from .. cp_handler import models as m


class AccessRight(models.Model):
    #charge_point = models.ForeignKey(to=m.ChargePoint, on_delete=models.CASCADE)
    user_account = models.ForeignKey(to='UserAccount', on_delete=models.CASCADE, null=True)
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    notes = models.TextField(null=True, blank=True)
    owns_charging_station = models.BooleanField(default=False)
    expiry_date = models.DateField(default=date(2021, 6, 28))
    # right_model_charge_point


class UserAccount(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    first_name = models.CharField(max_length=128)
    second_name = models.CharField(max_length=128)
    email = models.CharField(max_length=256)
    password = models.CharField(max_length=128)


class VehicleUsage(models.Model):
    user_account = models.ForeignKey(to='UserAccount', on_delete=models.CASCADE)
    electric_vehicle = models.ForeignKey(to='ElectricVehicle', on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, unique=True)


class ElectricVehicle(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=128)
    model = models.CharField(max_length=256)
    capacity = models.IntegerField()
    #socket_type = models.CharField(choices=enums.SocketType.choices, default=enums.SocketType.TYP2)
    max_current = models.FloatField(max_length=6, default=16.0)
    min_current = models.FloatField(max_length=6, default=16.0)
    set_power_limit = models.IntegerField(default=11000)
    soc = models.IntegerField()
