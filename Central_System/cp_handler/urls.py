from django.urls import path

from .views import index, chargepoint, chargepoint_detail, chargepoint_json, id_tag_info_json, call_reset

urlpatterns = [
    path('', index),
    path('chargepoint/', chargepoint),
    path('chargepoint/<str:slug>/', chargepoint_detail),
    path('cp/<str:slug>/', chargepoint_json),
    path('idtaginfo/', id_tag_info_json),
    path('call/call_reset/<str:cp_id>', call_reset)
]

