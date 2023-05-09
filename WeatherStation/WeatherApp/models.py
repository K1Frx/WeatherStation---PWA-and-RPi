from django.db import models
from django.utils import timezone

# Create your models here.

class Record(models.Model):
    date = models.DateTimeField(default = timezone.now)
    temperature = models.FloatField()
    pressure = models.FloatField()

    def __str__(self):
        return str(self.id) + ' - ' + str(self.date)