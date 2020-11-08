import mongoengine


class Measurand(mongoengine.Document):
    measurand = mongoengine.StringField(required=True)
    unit = mongoengine.StringField(required=True)
    value = mongoengine.FloatField(required=True)
    phase = mongoengine.StringField(default="null")


class MeterValue(mongoengine.Document):
    connector_id = mongoengine.IntField(default=1)
    transaction_id = mongoengine.IntField(required=False)
    power_active_import = mongoengine.EmbeddedDocumentListField(Measurand)
    energy_active_register = mongoengine.EmbeddedDocumentListField(Measurand)
    # this is so mongoengine knows where to put the data:
    meta = {'db_alias': 'core',
            'collection': 'meter_values'}


class HeartBeat(mongoengine.Document):
    pass


class BootNotification(mongoengine.Document):
    charge_point_model = mongoengine.StringField(required=True)
    charge_point_vendor = mongoengine.StringField(required=True)
    time_stamp = mongoengine.StringField(required=True)
