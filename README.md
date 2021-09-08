# sec-directory-server

This is the administration interface for the SEC Directory system. It's built on Django, utilizing docker to manage the build process and dependencies.

## App architecture

This application's primary purpose is to push directory data into a search index on Algolia. The main source for that data is the existing SEAS directory feed used for the www.seas.harvard.edu website; other people and places can be manually entered through the Django admin interface. Those three data sources are then compiled into a single "Rollup" data model, which is added to the Algolia index.

A separate [sec-directory-client][client] project hosts the applications public-facing code, with connects directly to Algolia to search and display results from the index.

## Local Development

For development, there is a [`docker-compose.yml`](docker-compose.yml) file in the root of the project. You'll need to copy the [`template.env`](template.env) file to `.env` and fill in the appropriate values for the database connection and the Algolia application and index.

For Algolia, you'll need to provide the `ALGOLIA_APP_ID` that owns the index defined in `ALGOLIA_INDEX`, and provide an `ALGOLIA_API_KEY` that has permission to `addObject`, `deleteObject` and `deleteIndex` for that same index. For security reasons, it's best [to create a "Secured API key"][api-key] scoped to the index, and we recommend using different indices for production, development, and testing.

With the `.env` file created, run:

```sh
$ docker-compose up
```

Which should bring up the app and database containers. From there, you can access the Django admin interface in the browser at http://localhost:8000/admin and log in with the credentials defined in the `DJANGO_SUPERUSER_USERNAME` and `DJANGO_SUPERUSER_PASSWORD` variables.

Our [`Dockerfile`](app/Dockerfile) uses a multi-stage build, and the `docker-compose` file targets the `development` stage, which has some additional system dependencies installed and runs the built-in Django web server. To install additional python dependencies, you should put them in [`app/requirements.txt`](app/requirements.txt) and rebuild the image with:

```sh
$ docker-compose build
```

To access Django's CLI tool, you can run:

```sh
$ docker-compose exec web python manage.py
```

That will list all of the available commands. For development the most important ones will be:

```sh
# Run tests
$ docker-compose exec web python manage.py test

# Run database migrations
$ docker-compose exec web python manage.py migrate

# Run the load_feed_people function to populate the Algolia index defined in ALGOLIA_INDEX
$ docker-compose exec web python manage.py shell --command "from feedperson.utils import load_feed_people; load_feed_people()"
```

## Running in Production

The docker image is built by [GitHub Action][actions] and [published through GitHub container registry][package]. To run the latest version of the app:

```sh
# Pull the latest copy of the image
$ docker pull ghcr.io/seas-computing/sec-directory-server:stable

# Run the image, passing through the necessary environment variables from our .env file
$ docker run -it --rm --env-file .env ghcr.io/seas-computing/sec-directory-server:stable
```

When running in production, the `DJANGO_SETTINGS_MODULE` environment variable should be set to `app.settings.production`. By default, the production image will run a `gunicorn` process that listens on port 8000.

There is also a [`docker-compose.prod.yml`](docker-compose.prod.yml) file that runs the container in production mode behind an nginx proxy. This is primarily useful for testing the production settings; our real production deployment will be using AWS Elastic Container Service, Relational Database Service, and Elastic Load Balancer.

To run in production mode, run:

```sh
$ docker-compose --file docker-compose.prod.yml up --build
```

Then visit http://localhost:1337/admin in the browser.

## Additional Commands

In addition to serving the administration interface, the Django can also run a function to import the directory feed and push that data to Algolia. In production, this is done through a separate task using the same container.

```sh
$ docker run -it --rm --env-file .env ghcr.io/seas-computing/sec-directory-server:stable python manage.py shell --command "from feedperson.utils import load_feed_people; load_feed_people()"
```

When running the container with an additional shell command like this, the [`app/entrypoint.sh` script](app/entrypoint.sh) will not run the `gunicorn` or development server processes; it will run the command specified within the `/app` directory in the container. If the `DATABASE` environment variable is set to `postgres`, it will wait for the database defined by `SQL_HOST` and `SQL_PORT` to become available before proceeding.

You can also force the container to run in production or development mode by passing `--production` or `--development` as the **only** arguments. For example:

```sh
# For Production mode
$ docker run -it --rm --env-file .env ghcr.io/seas-computing/sec-directory-server:stable --production

# For Development mode
$ docker run -it --rm --env-file .env ghcr.io/seas-computing/sec-directory-server:stable --development
```

With no arguments, the image will default to running in production mode.

[client]: https://github.com/seas-computing/sec-directory-client
[api-key]: https://www.algolia.com/doc/guides/security/api-keys/#secured-api-keys
[actions]: https://github.com/seas-computing/sec-directory-server/actions
[package]: https://github.com/seas-computing/sec-directory-server/pkgs/container/sec-directory-server
