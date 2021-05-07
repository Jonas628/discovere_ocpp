from django.urls import path

from .views import index, chargepoint, chargepoint_detail

urlpatterns = [
    path('', index),
    path('chargepoint/', chargepoint),
    path('chargepoint/<str:slug>', chargepoint_detail)
]

