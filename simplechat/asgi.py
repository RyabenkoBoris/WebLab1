import os

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from chat.middleware import TokenAuthMiddleware
from chat.routing import websocket_urlpatterns as chat_websocket_urlpatterns
from account.routing import websocket_urlpatterns as admin_websocket_urlpatterns

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'simplechat.settings')
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(URLRouter(chat_websocket_urlpatterns + admin_websocket_urlpatterns))
        ),
    }
)
