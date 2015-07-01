from django.core.exceptions import ValidationError
from django.db import models
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User

# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=500,blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True, null=True)
    activity_date = models.DateTimeField(blank=False)
    position = GeopositionField()
    place_name = models.CharField(max_length=150, blank=False)
    user_own = models.ForeignKey(User)
    parent = models.ForeignKey("self", null=True)
    price = models.FloatField(default=0.0)
    limit_participants = models.IntegerField(null=True)
    participants = models.ManyToManyField(User, through="Enrollment", related_name="participants")

class Enrollment(models.Model):
    activity = models.ForeignKey("Activity")
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("activity", "user"),)

#Validadores


