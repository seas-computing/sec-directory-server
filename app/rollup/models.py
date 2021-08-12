from django.db import models

# Create your models here.
class Rollup(models.Model):
  location = models.CharField(max_length=255)
  name = models.CharField(max_length=255)
