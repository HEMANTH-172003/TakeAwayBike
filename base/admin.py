from django.contrib import admin
from .models import *

# Register your models here.
class BikeAdmin(admin.ModelAdmin):
    list_display = ['id','bike_model']

admin.site.register(Bike,BikeAdmin)
