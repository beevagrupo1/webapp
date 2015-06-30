from django import forms
from geoposition.forms import GeopositionField
from datetime import date
from django.contrib.admin import widgets
from models import Activity

class ActivityForm(forms.ModelForm):
    activity_date = forms.DateField(initial=date.today())

    class Meta:
        model = Activity
        fields = ['title', 'description', 'activity_date', 'place_name', 'position', 'tags', 'price', 'limit_participants']
