from django.test import TestCase

from .models import Person

# Create your tests here.
class PersonTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    person = Person.objects.create(firstname="Jane", lastname="Harvard", location="SEC Room 322", name="Jane Harvard")

  def test_str_value(self):
    person = Person.objects.get(id=1)
    self.assertEqual(person.name, str(person))

  def test_first_name_label(self):
    person = Person.objects.get(id=1)
    label = person._meta.get_field('firstname').verbose_name
    self.assertEqual(label, 'First name')

  def test_last_name_label(self):
    person = Person.objects.get(id=1)
    label = person._meta.get_field('lastname').verbose_name
    self.assertEqual(label, 'Last name')

  def test_location_label(self):
    person = Person.objects.get(id=1)
    label = person._meta.get_field('location').verbose_name
    self.assertEqual(label, 'Location')
  
  def test_name_label(self):
    person = Person.objects.get(id=1)
    label = person._meta.get_field('name').verbose_name
    self.assertEqual(label, 'Full name')
