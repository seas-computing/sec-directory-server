from django.test import TestCase, Client
from django.contrib.auth.models import User
from algoliasearch_django.decorators import disable_auto_indexing
import requests
from unittest.mock import patch

from .models import Place

test_username = 'test'
test_email = 'test@test.com'
test_password = 'TesterPassword'
update_screens_button_label = 'Update screens'
success_message = 'Successfully updated screens with revised person and place data.'
error_message = 'Error: Unable to update screens. If the problem persists, contact SEAS Computing.'
c = Client()

# Create your tests here.
class PlaceTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    place = Place.objects.create(name="SEC", location="150 Western Ave, Allston, MA 02134")
    User.objects.create_superuser(test_username, test_email, test_password)
    c.login(username=test_username, password=test_password)
  
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
  
  def test_place_update_screens_button_renders(self):
    response = c.get('/admin/place/place/')
  
    self.assertEqual(response.status_code, 200)
    self.assertTrue(update_screens_button_label in response.content.decode('utf-8'))

  def test_click_place_update_screens_button_result(self):
    with disable_auto_indexing():
      response = c.get('/admin/place/place/actions/UpdateScreensButton/', follow=True)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(success_message in response.content.decode('utf-8'))
  
  @patch('rollup.utils.load_rollup')
  def test_click_place_update_screens_button_error(self, mock_load_rollup):
    mock_load_rollup.side_effect = Exception('Test error')
    with disable_auto_indexing():
      response = c.get('/admin/place/place/actions/UpdateScreensButton/', follow=True)
    self.assertTrue(error_message in response.content.decode('utf-8'))
