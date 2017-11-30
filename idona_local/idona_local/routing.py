from channels.routing import route
from idona.consumers import ws_connect, ws_disconnect, mqtt_message

channel_routing=[
    route('websocket.connect', ws_connect),
    route('websocket.disconnect', ws_disconnect),
    route('mqtt.sub', mqtt_message),
]
