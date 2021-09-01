from django.test import TestCase
from .models import FeedPerson
from feedperson.utils import load_feed_people
from algoliasearch_django.decorators import disable_auto_indexing

# Create your tests here.
class FeedPersonTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    feed_person = FeedPerson.objects.create(eppn="1a2b3c456def7890", firstname="John", lastname="Harvard", location="Pierce Hall 101", name="John Harvard")

  def test_str_value(self):
    feed_person = FeedPerson.objects.get(id=1)
    self.assertEqual(feed_person.name, str(feed_person))

class LoadFeedTest(TestCase):
  
  @classmethod
  def setUpTestData(cls):
    with disable_auto_indexing():
      load_feed_people()

  def test_load_feed_people_imports_western_ave_people(self):
    western_ave_people = filter(lambda person: "Western Ave" in person.location, FeedPerson.objects.all())
    non_western_ave_people = filter(lambda person: "Western Ave" not in person.location, FeedPerson.objects.all())
    self.assertTrue(len(list(western_ave_people)) > 0)
    self.assertEqual(len(list(non_western_ave_people)), 0)

  def test_load_feed_people_regex_removes_all_SciEnG(self):
    scieng_people = filter(lambda person: "Sci&Eng" in person.location, FeedPerson.objects.all())
    self.assertTrue(len(list(scieng_people)) == 0)

  def test_load_feed_people_regex_removes_all_western_avenue(self):
    western_avenue_people = filter(lambda person: "Western Avenue" in person.location, FeedPerson.objects.all())
    self.assertTrue(len(list(western_avenue_people)) == 0)

  def test_load_feed_people_removes_original_data(self):
    feed_person = FeedPerson.objects.create(eppn="1a2b3c456def7890", firstname="John", lastname="Harvard", location="Pierce Hall 101", name="John Harvard")
    with disable_auto_indexing():
      load_feed_people()
    self.assertEqual(FeedPerson.objects.filter(eppn=feed_person.eppn).count(), 0)