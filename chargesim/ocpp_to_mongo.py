import mongoengine


class MeterValue(mongoengine.Document):
    connector_id = mongoengine.IntField(default=1)
    meter_value = mongoengine.DictField(required=True)
    transaction_id = mongoengine.IntField(required=False)
    meta = {'db_alias': 'core',
            'collection': 'meter_values'}


class HeartBeat(mongoengine.Document):
    pass
