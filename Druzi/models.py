from unicodedata import decimal
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import permalink
from geoposition.fields import GeopositionField
from django.contrib.auth.models import User
from datetime import datetime
from django.utils.html import strip_tags
from django.utils import timezone
from django.template.defaultfilters import slugify

# Create your models here.
class Activity(models.Model):
    title = models.CharField(max_length=150, blank=False)
    description = models.TextField(max_length=500, blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True, null=True)
    activity_date = models.DateTimeField(blank=False)
    position = GeopositionField()
    place_name = models.CharField(max_length=150, blank=False)
    user_own = models.ForeignKey(User)
    parent = models.ForeignKey("self", null=True)
    price = models.FloatField(default=0.0)
    limit_participants = models.IntegerField(null=True, default=0)
    participants = models.ManyToManyField(User, default=0, through="Enrollment", related_name="participants")
    tags = models.ManyToManyField("Tag", through="TagAppear", related_name="tags")
    visit_count = models.IntegerField(default=0)
    sum_rating = models.FloatField(default=0.0)
    count_rating = models.IntegerField(default=0)

    def clone(self, user):
        return Activity(title=self.title, description=strip_tags(self.description), position=self.position,
                        place_name=self.place_name, parent=self, price=self.price,
                        limit_participants=self.limit_participants, user_own=user)

    @property
    def is_enable(self):
        a = timezone.now() - self.creation_date
        if a.total_seconds() < 5*60: #5*60 are 5 minutes
            return True
        return False    
    
    @property
    def is_open(self):
        if self.activity_date > timezone.now():
            return True
        return False

    @property
    def num_repeats(self):
        if self.parent == None:
            num = Activity.objects.filter(parent=self).count()
            return num
        else:
            num = Activity.objects.filter(parent=self.parent).count()
            return num

    @property
    def get_rating(self):
        if self.count_rating==0:
            return 0
        else:
            return float(self.sum_rating / self.count_rating).__format__("f")

    @property
    def get_description_text(self):
        return strip_tags(self.description)

    @property
    def get_id_repeat(self):
        if self.parent == None:
            return self.id
        else:
            return self.parent.id

    @property
    def get_keywords(self):
        keywords = ""
        for tag in self.tags.all():
            keywords = keywords.join(tag.name + ",")
        return keywords

    @property
    def get_slug(self):
        return slugify(self.title)
        
    @property
    def count_participantes(self):
        count_participants = self.participants.all().count()
        return count_participants

    @permalink
    def get_absolute_url(self):
        return ('activity_details', (),  {
            'slug': self.get_slug,
            'id': self.id,
        })

class Rating(models.Model):
    activity = models.ForeignKey("Activity")
    user = models.ForeignKey(User)
    creation_date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

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

# Validadores
