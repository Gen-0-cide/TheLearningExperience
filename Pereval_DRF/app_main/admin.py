from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(PerevalAdd)
admin.site.register(PerevalUser)
admin.site.register(Coords)
admin.site.register(Images)