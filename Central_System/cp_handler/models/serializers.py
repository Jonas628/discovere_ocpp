from ocpp_d.v16.enums import AuthorizationStatus
from rest_framework import serializers
from .models import ChargePoint, IdTagInfo, Connector


#from enumchoicefield import ChoiceEnum, EnumChoiceField

class ChargePointSerializer(serializers.ModelSerializer):

    class Meta:
        model = ChargePoint
        fields = '__all__'
        # fields = ('id', 'max_power')


class ConnectorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connector
        fields = '__all__'
        # fields = ('id', 'max_power')


class IdTagInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = IdTagInfo
        #expiry_date = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")
        #fields = ('expiry_date', 'parent_id_tag', 'status')
        exclude = ['id_tag']

    #status = serializers.ChoiceField(AuthorizationStatus)
    #status = EnumChoiceField(enum_class=AuthorizationStatus)
