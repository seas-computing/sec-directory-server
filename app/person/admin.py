from django.contrib import admin
from rollup.utils import load_rollup, UpdateScreens
from .models import Person

admin.site.register(Person, UpdateScreens)
