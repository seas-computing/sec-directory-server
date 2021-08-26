from django.contrib import admin, messages
from rollup.utils import load_rollup
from django_object_actions import DjangoObjectActions
from .models import Person

# Adds a button to the Person Admin page to allow users to manually update the
# directory screens with the most up-to-date data
class PersonAdmin(DjangoObjectActions, admin.ModelAdmin):

  def UpdateScreens(self, request, queryset):
    load_rollup()
    self.message_user(request, 'Successfully updated screens with revised person and place data.', level=messages.SUCCESS, fail_silently=False)
  
  UpdateScreens.label = 'Update screens'
        
  changelist_actions = ('UpdateScreens', )

admin.site.register(Person, PersonAdmin)
