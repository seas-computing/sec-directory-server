from django.test import TestCase

from .models import FeedPerson

# Create your tests here.
class FeedPersonTestCase(TestCase):

  def setUp(self):
    feed_person = FeedPerson.objects.create(eppn="1a2b3c456def7890", firstname="John", lastname="Harvard", location="Pierce Hall 101", name="John Harvard")

  def test_str_value(self):
    feed_person = FeedPerson.objects.get(id=1)
    self.assertEqual(feed_person.name, str(feed_person))
