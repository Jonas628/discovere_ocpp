from ocpp_d.charge_point import ChargePoint as cp
from ocpp_d.v201 import call_result, call


class ChargePoint(cp):
    _call = call
    _call_result = call_result
    _ocpp_version = '2.0.1'
