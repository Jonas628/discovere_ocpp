from django.db import models
from django.utils.translation import gettext_lazy as _
from ocpp_d.v16.enums import AuthorizationStatus

"""
the foreign key must be part of the object B if relationship A - B = 1 : N
"""


# ENUMS
class PhaseRotation(models.TextChoices):
    RST = 'RST', _('RST')
    STR = 'STR', _('STR')
    TRS = 'TRS', _('TRS')
    RTS = 'RTS', _('RTS')
    SRT = 'SRT', _('SRT')
    TSR = 'TSR', _('TSR')
    # add choices for 1 and 2 phases


class SocketType(models.TextChoices):
    TYP1 = 'TYP1', _('Typ_1')
    TYP2 = 'TYP2', _('Typ_2')
    CCS = 'CCS', _('CCS')


class BackendProtocol(models.TextChoices):
    OCPP16_J = 'OCPP16_J', _('OCPP_1.6_JSON')
    OCPP20_J = 'OCPP20_J', _('OCPP_2.0_JSON')
    OCPP201_J = 'OCPP201_J', _('OCPP_2.0.1_JSON')


"""
class AuthorizationStatus(models.TextChoices):
    ACCEPTED = 'ACCAPTED', _('accapted')
    BLOCKED = 'BLOCKED', _('blocked')
    CONCURRENT = 'CONCURRENT', _('concurrent_tx')
    EXPIRED = 'EXPIRED', _('expired')
    INVALID = 'INVALID', _('invalid')
"""




