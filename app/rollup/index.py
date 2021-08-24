import algoliasearch_django as algoliasearch

from .models import Rollup

algoliasearch.register(Rollup)
