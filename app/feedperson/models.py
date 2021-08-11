from django.db import models

# Create your models here.
class FeedPerson(models.Model):
  eppn = models.CharField(max_length=255, blank=True, null=True)
  firstname = models.CharField(max_length=255, blank=True, null=True)
  lastname = models.CharField(max_length=255, blank=True, null=True)
  location = models.CharField(max_length=255, blank=True, null=True)
  name = models.CharField(max_length=255, blank=True, null=True)

  def __str__(self):
    return self.name
