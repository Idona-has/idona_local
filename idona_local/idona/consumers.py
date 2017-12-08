from channels import Group

from django.core.exceptions import ObjectDoesNotExist
from .models import Device, Endpoint

def ws_connect(message):
    Group('users').add(message.reply_channel)

def ws_disconnect(message):
    Group('users').discard(message.reply_channel)

def mqtt_message(message):
    bits=message['topic'].split('/',5)
    assert len(bits)==6
    deviceId,endpointId=bits[4:6]

    try:
        endpoint=Endpoint.objects.get(ID=endpointId, device=deviceId)
        endpoint.value=message['payload']
    except ObjectDoesNotExist: pass
