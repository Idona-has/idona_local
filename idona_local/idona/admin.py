from django.contrib import admin
from .models import *

@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin): pass

@admin.register(Endpoint)
class EndpointAdmin(admin.ModelAdmin): pass
