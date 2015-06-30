from django.contrib import admin
from .models import Tag,Activity,Enrollment

# Register your models here.
admin.site.register(Tag)
admin.site.register(Activity)
admin.site.register(Enrollment)