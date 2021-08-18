from feedperson.models import FeedPerson
from urllib.request import urlopen
import re
from bs4 import BeautifulSoup
from django.http import HttpResponse
from rollup.utils import load_rollup

def load_feed_people():
  # Remove the existing FeedPerson data before importing updated data
  FeedPerson.objects.all().delete()

  with urlopen('https://nodefeeds.seas.harvard.edu/app/api/person/list/active') as file:
    feed_contents = file.read().decode('utf-8')

  soup = BeautifulSoup(feed_contents, 'html.parser')

  people = soup.findAll('person')

  for person in people:
    location = person.location.fordisp.text
    if (re.match('114 Western Ave', location) or re.match('150 Western Ave', location)):
      FeedPerson.objects.create(
        eppn=person.eppn.text,
        firstname=person.givenname.text,
        lastname=person.lastname.text,
        name=person.gecos.text,
        location=location
      )
  
  load_rollup()

