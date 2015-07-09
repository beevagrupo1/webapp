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
    participants = models.ManyToManyField(User, default=0, through="Enrollment", related_name="participants")
    tags = models.ManyToManyField("Tag", through="TagAppear", related_name="tags")

    visit_count = models.IntegerField(default=0)

class Tag(models.Model):
    name = models.CharField(max_length=50, primary_key=True)
    count = models.IntegerField(default=0)
    activity = models.ManyToManyField("Activity", through="TagAppear", related_name="activities")

class TagAppear(models.Model):
    activity = models.ForeignKey("Activity")
    tag = models.ForeignKey("Tag")
    position = models.IntegerField()

class Enrollment(models.Model):
    activity = models.ForeignKey("Activity")
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = (("activity", "user"),)

#Validadores


