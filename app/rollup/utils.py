from .models import Rollup
from place.models import Place
from person.models import Person
from feedperson.models import FeedPerson

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
