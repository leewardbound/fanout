from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import re_path

class WebsocketConsumer(AsyncJsonWebsocketConsumer):
    ################################
    # Connect / Disconnect
    ################################
    async def connect(self):
        await self.accept()
        await self.send_json({"connected": True})

    async def disconnect(self, code):
        await self.close()


application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),

        # WebSocket chat handler
        "websocket": AuthMiddlewareStack(
            URLRouter([re_path(r"ws/", WebsocketConsumer),])
        )
    }
)
