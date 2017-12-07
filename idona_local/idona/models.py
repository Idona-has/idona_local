from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

from channels import Channel

class Device(models.Model):
    ID=models.CharField(max_length=12, primary_key=True)

@receiver(post_save, sender=Device)
def devicePostSave(sender, instance, created, *args, **kwargs):
    if not created: return

    for ep in (0,1,2,3,4,5,6,7,8,91,92,99,):
        Endpoint(ID=ep, device=instance).save()

class Endpoint(models.Model):
    SYSTEM=0
    BINARY_OUTPUT=1
    INTEGER_OUTPUT=2
    BINARY_INPUT=3
    DECIMAL_INPUT=4
    INTEGER_INPUT=5
    STRING=6
    _RESERVED_=7
    ERROR=8

    SYSTEM_RANGE=range(0,16)
    BINARY_OUTPUT_RANGE=range(16,32)
    INTEGER_OUTPUT_RANGE=range(32,40)
    BINARY_INPUT_RANGE=range(40,48)
    DECIMAL_INPUT_RANGE=range(48,64)
    INTEGER_INPUT_RANGE=range(64,72)
    STRING_RANGE=range(72,73)
    _RESERVED__RANGE=range(73,91)
    ERROR_RANGE=range(91,100)

    VALUE_TYPES=(
        (SYSTEM,'System'),
        (BINARY_OUTPUT,'Binary Output'),
        (INTEGER_OUTPUT,'Integer Output'),
        (BINARY_INPUT,'Binary Input'),
        (DECIMAL_INPUT,'Decimal Input'),
        (INTEGER_INPUT,'Integer Input'),
        (STRING,'String'),
        (_RESERVED_,'¡Reserved!'),
        (ERROR,'Error')
    )

    class Meta:
        unique_together=(('id','device'),)

    ID=models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    device=models.ForeignKey(Device, on_delete=models.CASCADE)
    readOnly=models.BooleanField(default=True)
    type=models.PositiveSmallIntegerField(choices=VALUE_TYPES)

    binaryValue=models.BinaryField(default=False)
    integerValue=models.IntegerField(default=0)
    decimalValue=models.FloatField()
    stringValue=models.CharField(max_length=256)

    def topic(self, direction="sb"):
        return "/idona/local/{}/{}/{}".format(direction, self.device.ID, self.ID)

    def save(self, *args, **kwargs):
        if not self.type:
            if self.ID in self.SYSTEM_RANGE: self.type=self.SYSTEM
            elif self.ID in self.BINARY_OUTPUT_RANGE: self.type=self.BINARY_OUTPUT
            elif self.ID in self.INTEGER_OUTPUT_RANGE: self.type=self.INTEGER_OUTPUT
            elif self.ID in self.BINARY_INPUT_RANGE: self.type=self.BINARY_INPUT
            elif self.ID in self.DECIMAL_INPUT_RANGE: self.type=self.DECIMAL_INPUT
            elif self.ID in self.INTEGER_INPUT_RANGE: self.type=self.INTEGER_INPUT
            elif self.ID in self.STRING_RANGE: self.type=self.STRING
            elif self.ID in self._RESERVED__RANGE: self.type=self._RESERVED_
            elif self.ID in self.ERROR_RANGE: self.type=self.ERROR
            else: self.type=0
        super().save(*args, **kwargs)

    def read(self):
        Channel('mqtt.pub').send(dict(topic=self.topic(), payload="READ"))

    def write(self):
        Channel('mqtt.pub').send(dict(topic=self.topic(), payload=self.value))

    @property
    def value(self):
        if self.type in (self.BINARY_INPUT,self.BINARY_OUTPUT): return str(self.binaryValue)
        elif self.type in (self.INTEGER_INPUT, self.INTEGER_OUTPUT): return str(self.integerValue)
        elif self.type==self.DECIMAL_INPUT: return str(self.DECIMAL_INPUT)
        elif self.type==self.STRING: return  self.stringValue
        return None

    @value.setter
    def value(self, value):
        if self.ID in (self.BINARY_INPUT,self.BINARY_OUTPUT):
            if str(value).lower() in ('false','off','0'): self.binaryValue=False
            elif str(value).lower() in ('true','on','1'): self.binaryValue=True
            else: return
        elif self.ID==self.DECIMAL_INPUT:
            try: self.decimalValue=float(value)
            except ValueError: return
        elif self.ID in (self.INTEGER_INPUT,self.INTEGER_OUTPUT):
            try: self.integerValue=int(value)
            except ValueError: return
        elif self.ID in self.STRING:
            self.stringValue=str(value)
        self.save()
