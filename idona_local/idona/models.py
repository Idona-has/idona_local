from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

class Device(models.Model):
    ID=models.CharField(max_length=12, primary_key=True)

@receiver(post_save, sender=Device)
def devicePostSave(sender, instance, created, *args, **kwargs):
    if not created: return

    for ep in (0,1,2,3,4,5,6,7,8,91,92,99,):
        Endpoint(ID=ep, device=instance).save()

class Endpoint(models.Model):
    VALUE_TYPES=(
        (0,'System'),
        (1,'Binary Output'),
        (2,'Integer Output'),
        (3,'Binary Input'),
        (4,'Decimal Input'),
        (5,'Integer Input'),
        (6,'String'),
        (7,'¡Reserved!'),
        (8,'Error')
    )

    class Meta:
        unique_together=(('id','device'),)

    ID=models.PositiveSmallIntegerField(validators=[MinValueValidator(0), MaxValueValidator(99)])
    device=models.ForeignKey(Device, on_delete=models.CASCADE)
    readOnly=models.BooleanField(default=True)
    type=models.PositiveSmallIntegerField(choices=VALUE_TYPES)

    def topic(self, direction="sb"):
        return "/idona/local/{}/{}/{}".format(direction, self.device.ID, self.ID)

    def save(self, *args, **kwargs):
        if not self.type:
            if 0<=self.ID<=15: self.type=0
            elif 90<=self.ID<=99 : self.type=8
            else: self.type=0
        super().save(*args, **kwargs)