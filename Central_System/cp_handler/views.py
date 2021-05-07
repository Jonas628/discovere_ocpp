from django.shortcuts import render, get_object_or_404

from django.http import HttpResponse, HttpResponseRedirect

from django.urls import reverse
from django.views import generic

from django.contrib import messages

from .models import ChargePoint


def index(request):
    return render(request, template_name='index.html', context={'text': 'Hello World'})

def chargepoint(request):
    context = {'chargepoints': ChargePoint.objects.all()}
    return render(request=request, template_name='cp_overview.html', context=context)

def chargepoint_detail(request, slug):
    chargepoint = ChargePoint.objects.get(slug=slug)
    context = {'chargepoint': chargepoint}
    return render(request=request, template_name='cp_details.html', context=context)

"""
    charge_point_name = ""
    for cp in ChargePoint.objects.all():
        charge_point_name = charge_point_name + "<br /> " + cp.name
    return HttpResponse(charge_point_name)
"""

