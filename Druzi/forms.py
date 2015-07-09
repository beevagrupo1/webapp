from django import forms
from geoposition.forms import GeopositionField
from datetime import date
from django.contrib.admin import widgets
from models import Activity
from bootstrap3_datetime.widgets import DateTimePicker
from django import forms

class ActivityForm(forms.ModelForm):
    activity_date = forms.DateTimeField(
        required=False,
        widget=DateTimePicker(options={"format": "YYYY-MM-DD HH:mm",
                                       "pickSeconds": False}))

    class Meta:
        model = Activity
        fields = ['title', 'description', 'activity_date', 'place_name', 'position', 'price', 'limit_participants']
