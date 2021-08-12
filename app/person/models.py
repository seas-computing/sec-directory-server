from django.db import models

# Create your models here.
class Person(models.Model):
  firstname = models.CharField('First name', max_length=255)
  lastname = models.CharField('Last name', max_length=255)
  location = models.CharField('Location', max_length=255)
  name = models.CharField('Full name', max_length=255)
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name_plural = 'People'
