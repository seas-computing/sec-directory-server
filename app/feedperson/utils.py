from feedperson.models import FeedPerson
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from django.http import HttpResponse
from rollup.utils import load_rollup
from rollup.index import RollupIndex
from algoliasearch_django.decorators import disable_auto_indexing

def load_feed_people():
  print("Beginning load_feed_people")
  # Remove the existing FeedPerson data before importing updated data
  print('Beginning to delete existing people')
  FeedPerson.objects.all().delete()
  print('Done deleting existing people')

  print('fetching data from nodefeeds')
  with urlopen('https://nodefeeds.seas.harvard.edu/app/api/person/list/active') as file:
    feed_contents = file.read().decode('utf-8')

  soup = BeautifulSoup(feed_contents, 'html.parser')

  print('parsing people from data')
  people = soup.findAll('person')
  print('Found ' + str(len(people)) + ' total people');
  counter = 0;
  for person in people:
    location = person.location.fordisp.text
    if (re.match('114 Western Ave', location) or re.match('150 Western Ave', location)):
      # This regex is a temp fix whilst the location data is inconsistent in PeopleSoft.
      # Should be removed once the data is fixed.
      if re.match('150 Western Ave', location):
        location = re.sub(r'Sci&Eng', 'SEC', location)

        # This allows for multiple spaces between words, and it allows the pattern to be "150 Western Ave", "150 Western Ave.", or "150 Western Avenue".
        # Also, in case the original string already contains "SEC," we include "SEC" in the pattern so that the result does not have "SEC" twice
        # (e.g. "150 Western Ave, SEC, SEC" as the final resulting string)
        location = re.sub(r'\b150\s+Western\s+Ave(?:\.|nue)?(?:,\s*SEC)?', "150 Western Ave. SEC", location, flags=re.IGNORECASE)
      counter += 1
      print('Importing ' + person.gecos.text)
      FeedPerson.objects.create(
        eppn=person.eppn.text,
        firstname=person.givenname.text,
        lastname=person.lastname.text,
        name=person.gecos.text,
        location=location
      )
  print('Loaded ' + str(counter) + ' people in Allston')

  load_rollup()
  print('Done with load_feed_people')
