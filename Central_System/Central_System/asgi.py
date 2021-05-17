"""
ASGI config for Central_System project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

from channels.routing import ProtocolTypeRouter
from channels.routing import URLRouter
from channels.auth import AuthMiddlewareStack

import cp_handler.routing


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Central_System.settings')

application = ProtocolTypeRouter({
    'http': get_asgi_application(),

    'websocket': AuthMiddlewareStack(
        URLRouter(
            cp_handler.routing.ws_urlpatterns
        ))
})
