from django.db import models

# Create your models here.
class Place(models.Model):
  name = models.CharField('Place name', max_length=255, blank=False, null=False)
  location = models.CharField('Location', max_length=255, blank=False, null=False)

  def __str__(self):
    return self.name
