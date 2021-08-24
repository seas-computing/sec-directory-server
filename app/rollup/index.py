import algoliasearch_django as algoliasearch
from algoliasearch_django.decorators import register
from .models import Rollup
from os import environ

@register(Rollup)
class RollupIndex(algoliasearch.AlgoliaIndex):
  settings = {'searchableAttributes': ['name']}
  index_name = environ.get("ALGOLIA_INDEX")
