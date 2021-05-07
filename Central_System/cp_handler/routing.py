from django.urls import path


from .consumers import WSConsumer
from .CPconsumer import CPConsumer


ws_urlpatterns = [
    path('ws/some_url/', WSConsumer.as_asgi()),
    path('CP_1/', CPConsumer.as_asgi())
    # (url, handler)
]

# 'ws://localhost:8000/CP_1',
#          subprotocols=['ocpp1.6']
