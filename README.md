# sec-directory-server

This is the administration interface for the SEC Directory system. It's built on Django, utilizing docker to manage the build process and dependencies.

## App architecture

This application's primary purpose is to push directory data into a search index on Algolia. The main source for that data is the existing SEAS directory feed used for the www.seas.harvard.edu website; other people and places can be manually entered through the Django admin interface. Those three data sources are then compiled into a single "Rollup" data model, which is added to the Algolia index.

A separate [sec-directory-client][client] project hosts the applications public-facing code, with connects directly to Algolia to search and display results from the index.

## Django Tasks

In addition to serving the administration interface, the Django app run some recurring tasks:

- Importing and parsing the directory feed
- Pushing the Data to the Algolia index

**More details on those tasks and how they'll run in production, to come...**

## Docker Setup

### Development

For development, there is a `docker-compose.yml` file in the root of the project. You'll need to copy the `template.env.dev` file to `.env` and fill in the appropriate values for the database connection and the Algolia application and index.

For Algolia, you'll need to provide the `ALGOLIA_APP_ID` that owns the index defined in `ALGOLIA_INDEX`, and provide an `ALGOLIA_API_KEY` that has permission to `addObject`, `deleteObject` and `deleteIndex` for that same index. For security reasons, it's best [to create a "Secured API key"][api-key] scoped to the index.

With the `.env` file in place, run:

```sh
$ docker-compose up
```

Which should bring up the app and database containers. From there, you can access the Django admin interface in the browser at http://localhost:8000/admin and log in with the credentials defined in the `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` variables.

To access Django's CLI tool, you can run:

```sh
$docker-compose exec web python manage.py
```

That will list all of the available commands, but for development the most important ones will be:

```sh
# Run tests
$ docker-compose exec web python manage.py test

# Run database migrations
$ docker-compose exec web python manage.py migrate
```

### Production

There is also a `docker-compose.prod.yml` file that simulates launching the app in production mode behind an nginx proxy. This can be useful for testing, though for our real production deployment we'll be using AWS Elastic Container Service, Relational Database Service, and Elastic Load Balancer.

To run in production mode, run `docker-compose --file docker-compose.yml up`, then visit localhost:1337/admin in the browser

[client]: https://github.com/seas-computing/sec-directory-client
[api-key]: https://www.algolia.com/doc/guides/security/api-keys/#secured-api-keys
