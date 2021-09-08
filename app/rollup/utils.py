from django.contrib import admin, messages
from django_object_actions import DjangoObjectActions
from .models import Rollup
from place.models import Place
from person.models import Person
from feedperson.models import FeedPerson
import logging

# Creates updated Rollup objects using Place, Person, and FeedPerson data
def load_rollup():
  Rollup.objects.all().delete()
  places = Place.objects.all()
  people = Person.objects.all()
  feed_people = FeedPerson.objects.all()

  for objects in [places, people, feed_people]:
    for object in objects:
      Rollup.objects.create(
        name = object.name,
        location = object.location
      )

# Get an instance of a logger
logger = logging.getLogger(__name__)

class UpdateScreens(DjangoObjectActions, admin.ModelAdmin):

  def UpdateScreensButton(self, request, queryset):
    try:
      load_rollup()
      self.message_user(request, 'Successfully updated screens with revised person and place data.', level=messages.SUCCESS, fail_silently=False)
    except Exception as err:
      logger.exception(err)
      self.message_user(request, 'Error: Unable to update screens. If the problem persists, contact SEAS Computing.', level=messages.ERROR, fail_silently=False)
    
  UpdateScreensButton.label = 'Update screens'

  UpdateScreensButton.short_description = 'Manually refresh the screens with the most recent data.'
        
  changelist_actions = ('UpdateScreensButton', )
