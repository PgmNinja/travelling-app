from django.contrib import admin
from .models import *

# Register your models here.
for model in [Users, Location, Flight, Hotel, Package, Review]:

    admin.site.register(model)
