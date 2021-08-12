from django.test import TestCase

from .models import Place

# Create your tests here.
class PlaceTestCase(TestCase):

  def setUp(self):
    place = Place.objects.create(name="SEC", location="150 Western Ave, Allston, MA 02134")
  
  def test_str_value(self):
    place = Place.objects.get(id=1)
    self.assertEqual(place.name, str(place))

  def test_name_label(self):
    place = Place.objects.get(id=1)
    label = place._meta.get_field('name').verbose_name
    self.assertEqual(label, 'Place name')

  def test_location_label(self):
    place = Place.objects.get(id=1)
    label = place._meta.get_field('location').verbose_name
    self.assertEqual(label, 'Location')
