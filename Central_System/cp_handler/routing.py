from django.urls import path

from .CPconsumer import CPConsumer


ws_urlpatterns = [
    path('<str:id>/', CPConsumer.as_asgi()),
    #path('CP/<str:id>', CPConsumer(1).as_asgi()),
    # (url, handler)
]