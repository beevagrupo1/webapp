from django.contrib import admin
from .models import Activity,Enrollment, Review

# Register your models here.
admin.site.register(Activity)
admin.site.register(Enrollment)
admin.site.register(Review)