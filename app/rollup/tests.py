from django.test import TestCase
from rollup.utils import load_rollup
from rollup.models import Rollup
from place.models import Place
from person.models import Person
from feedperson.models import FeedPerson

# Create your tests here.
class RollupTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    # Existing Rollup objects that should be deleted after calling load_rollup
    Rollup.objects.create(name="John Smith", location="SEC Room 210")
    Rollup.objects.create(name="Jane Smith", location="SEC Room 142")
    Rollup.objects.create(name="SEC", location="150 Western Ave, Allston, MA 02134")
    Rollup.objects.create(name="114 Western Ave", location="114 Western Ave, Allston, MA 02134")
    # Data that should be converted to Rollup objects after calling load_rollup
    place = Place.objects.create(name="Soldier's Field Park Children's Center", location="114 Western Ave, Allston, MA 02134")
    person = Person.objects.create(firstname="Jane", lastname="Harvard", location="SEC Room 322", name="Jane Harvard")
    feed_person = FeedPerson.objects.create(eppn="1a2b3c456def7890", firstname="John", lastname="Harvard", location="Pierce Hall 101", name="John Harvard")
    load_rollup()

  def test_rollup_removes_original_data(self):
    self.assertEqual(Rollup.objects.filter(name="John Smith").count(), 0)
    self.assertEqual(Rollup.objects.filter(name="Jane Smith").count(), 0)
    self.assertEqual(Rollup.objects.filter(name="SEC").count(), 0)
    self.assertEqual(Rollup.objects.filter(name="114 Western Ave").count(), 0)
  
  def test_final_rollup_object_count(self):
    self.assertEqual(Rollup.objects.all().count(), 3)

  def test_new_data_present(self):
    self.assertEqual(Rollup.objects.filter(name="Soldier's Field Park Children's Center").count(), 1)
    self.assertEqual(Rollup.objects.filter(name="Jane Harvard").count(), 1)
    self.assertEqual(Rollup.objects.filter(name="John Harvard").count(), 1)
