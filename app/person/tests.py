from django.test import TestCase, Client
from django.contrib.auth.models import User
from algoliasearch_django.decorators import disable_auto_indexing
import requests
from unittest.mock import patch

from .models import Person

test_username = 'test'
test_email = 'test@test.com'
test_password = 'TesterPassword'
update_screens_button_label = 'Update screens'
success_message = 'Successfully updated screens with revised person and place data.'
error_message = 'Error: Unable to update screens. If the problem persists, contact SEAS Computing.'
c = Client()

# Create your tests here.
class PersonTestCase(TestCase):

  @classmethod
  def setUpTestData(cls):
    person = Person.objects.create(firstname="Jane", lastname="Harvard", location="SEC Room 322", name="Jane Harvard")
    User.objects.create_superuser(test_username, test_email, test_password)
    c.login(username=test_username, password=test_password)

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
  
  def test_person_update_screens_button_renders(self):
    response = c.get('/admin/person/person/')
  
    self.assertEqual(response.status_code, 200)
    self.assertTrue(update_screens_button_label in response.content.decode('utf-8'))

  def test_click_person_update_screens_button_successful_result(self):
    with disable_auto_indexing():
      response = c.get('/admin/person/person/actions/UpdateScreensButton/', follow=True)

    self.assertEqual(response.status_code, 200)
    self.assertTrue(success_message in response.content.decode('utf-8'))

  @patch('rollup.utils.load_rollup')
  def test_click_person_update_screens_button_error(self, mock_load_rollup):
    mock_load_rollup.side_effect = Exception('Test error')
    with disable_auto_indexing():
      response = c.get('/admin/person/person/actions/UpdateScreensButton/', follow=True)
    self.assertTrue(error_message in response.content.decode('utf-8'))
