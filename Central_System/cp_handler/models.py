from django.db import models
from . enums import enums

"""
the foreign key must be part of the object B if relationship A - B = 1 : N
"""


class ChargingStation(models.Model):
    id = models.IntegerField(primary_key=True, unique=True)
    name = models.CharField(max_length=256)
    position = models.TextField(null=True, blank=True)
    phase_rotation = models.CharField(max_length=3, choices=enums.PhaseRotation.choices, default=enums.PhaseRotation.RST)
    installation_date = models.DateTimeField()
    max_current = models.FloatField(max_length=6, default=16.0)
    # operating_status =


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
    protocol = models.CharField(max_length=10, choices=enums.BackendProtocol.choices, default=enums.BackendProtocol.OCPP16_J)

    def __str__(self):
        return "{0}: {1}".format(self.charging_station.name, self.name)


class Connector(models.Model):
    charge_point = models.ForeignKey(to='ChargePoint', on_delete=models.CASCADE)
    id = models.IntegerField(primary_key=True, default=0)
    socket_type = models.CharField(max_length=4, choices=enums.SocketType.choices, default=enums.SocketType.TYP2)
    max_current = models.FloatField(max_length=6, default=16.0)
    set_power_limit = models.IntegerField(default=11000)
    phase_rotation = models.CharField(max_length=3, choices=enums.PhaseRotation.choices, default=enums.PhaseRotation.RST)


class ChargePointConfiguration(models.Model):
    charge_point = models.ForeignKey(to='ChargePoint', on_delete=models.CASCADE)


"""
class Musician(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    instrument = models.CharField(max_length=100)

class Album(models.Model):
    artist = models.ForeignKey(Musician, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    release_date = models.DateField()
    num_stars = models.IntegerField()
    

from django.utils.translation import gettext_lazy as _

class Student(models.Model):

    class YearInSchool(models.TextChoices):
        FRESHMAN = 'FR', _('Freshman')
        SOPHOMORE = 'SO', _('Sophomore')
        JUNIOR = 'JR', _('Junior')
        SENIOR = 'SR', _('Senior')
        GRADUATE = 'GR', _('Graduate')

    year_in_school = models.CharField(
        max_length=2,
        choices=YearInSchool.choices,
        default=YearInSchool.FRESHMAN,
    )

    def is_upperclass(self):
        return self.year_in_school in {
            self.YearInSchool.JUNIOR,
            self.YearInSchool.SENIOR,
        }
"""
