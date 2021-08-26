from os import environ
from .models import Rollup
from place.models import Place
from person.models import Person
from feedperson.models import FeedPerson
from algoliasearch.search_client import SearchClient

# Forcees a clear-out of the index before reindexing.
# Prevents duplicate records being created if updates are pushed from two different DBs.
# This could happen if the production machine / DB are rebuilt.
def clear_index():
  client = SearchClient.create(environ.get("ALGOLIA_APP_ID"), environ.get("ALGOLIA_API_KEY"))
  index = client.init_index(environ.get("ALGOLIA_INDEX"))
  index.clear_objects()

# Creates updated Rollup objects using Place, Person, and FeedPerson data
def load_rollup():
  clear_index()
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
