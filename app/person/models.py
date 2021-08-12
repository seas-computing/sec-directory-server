from django.db import models

# Create your models here.
class Person(models.Model):
  firstname = models.CharField('First name', max_length=255, blank=False, null=False)
  lastname = models.CharField('Last name', max_length=255, blank=False, null=False)
  location = models.CharField('Location', max_length=255, blank=False, null=False)
  name = models.CharField('Full name', max_length=255, blank=False, null=False)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'People'
