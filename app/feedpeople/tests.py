from django.test import TestCase

from .models import FeedPerson

# Create your tests here.
class FeedPersonTestCase(TestCase):

  def setUp(self):
    feed_person = FeedPerson.objects.create(eppn="00000000", firstname="John", lastname="Harvard", location="Pierce Hall 101", name="John Harvard")

  def test_str_value(self):
    feed_person = FeedPerson.objects.get(id=1)
    expected = f"{feed_person.firstname} {feed_person.lastname}"
    self.assertEqual(expected, str(feed_person))
