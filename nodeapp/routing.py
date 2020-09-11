from django.conf.urls import url
from . import ssh_consumers

websocket_urlpatterns = [
    url(r'^ws/nodeapp/terminal_routing/(?P<nodeID>[^/]+)',ssh_consumers.SSHConsumer),
]
