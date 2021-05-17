import json

from django.http import JsonResponse
from django.shortcuts import render
from ocpp_d.v16 import call
from ocpp_d.v16.enums import ResetType

from rest_framework.renderers import JSONRenderer

from cp_handler.CPconsumer import consumer_map
from cp_handler.models.models import ChargePoint, Connector, IdTagInfo
from cp_handler.models.serializers import ChargePointSerializer, ConnectorSerializer, IdTagInfoSerializer


def index(request):
    return render(request, template_name='index.html', context={'text': 'Hello World'})


def chargepoint(request):
    context = {'chargepoints': ChargePoint.objects.all()}
    return render(request=request, template_name='cp_overview.html', context=context)


def chargepoint_detail(request, slug):
    chargepoint = ChargePoint.objects.get(slug=slug)
    context = {'chargepoint': chargepoint}
    return render(request=request, template_name='cp_details.html', context=context)


def chargepoint_json(request, slug):
    serializer = ChargePointSerializer(ChargePoint.objects.get(slug=slug))
    #serializer = ConnectorSerializer(Connector.objects.first())
    print("***: {0}".format(serializer.data))
    return JsonResponse(serializer.data)


def id_tag_info_json(request):
    serializer = IdTagInfoSerializer(IdTagInfo.objects.first())
    #data = json.dumps(serializer.data)
    print("***: {0}".format(serializer.data))
    #print("***: {0}".format(data))
    return JsonResponse(serializer.data)


async def call_reset(request, cp_id):
    _consumer = consumer_map.get_consumer(cp_id)
    print("send Reset-message to CP")
    payload = call.ResetPayload(type=ResetType.soft)
    print(payload)
    response = await _consumer._charge_point.call(payload)
    print(response)


"""
def message(request):
    context = {'message': ChargePoint.objects.all()}
    return render(request=request, template_name='cp_overview.html', context=context)
"""
