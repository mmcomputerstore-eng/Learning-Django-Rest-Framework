INVENTORY MANAGEMENT API

Project Overview

Inventory Management API is a Django REST Framework backend project for
managing products and stock. It provides API endpoints for product CRUD
operations, stock updates, authentication, filtering, searching,
ordering, and paginated results.

Technology Stack

-   Python
-   Django
-   Django REST Framework
-   PostgreSQL
-   Simple JWT authentication
-   django-filter
-   drf-spectacular (OpenAPI / Swagger documentation)
-   Gunicorn
-   WhiteNoise
-   python-decouple for environment variables

Main Features

-   Create, retrieve, update, partially update, and delete products.
-   Associate products with their owner.
-   Set the authenticated user as the owner when creating a product.
-   Validate product names, prices, and stock values.
-   Provide custom actions to increase or decrease product stock.
-   Support search and filtering for product data.
-   Support ordering by selected product fields.
-   Use pagination for product lists.
-   Protect API endpoints with authentication and permissions.
-   Use JWT access/refresh tokens.
-   Provide automated tests for important API behavior.
-   Provide API schema and Swagger documentation.
-   Use PostgreSQL for the database.
-   Use environment variables for sensitive and environment-specific
    settings.

Project Structure

config/ Django project settings, root URLs, ASGI and WSGI configuration.

core/ Product model, serializers, views/viewsets, permissions,
pagination, URLs, and tests.

manage.py Django management command entry point.

requirements.txt Python dependencies.

build.sh Build script that collects static files and runs database
migrations.

DEPLOYMENT.md Deployment preparation notes.

schema.yml OpenAPI schema file, if kept up to date in the repository.

Setup Instructions

1.  Install Python and Git.

2.  Clone the repository: git clone cd

3.  Create and activate a virtual environment.

    On Ubuntu/Linux: python3 -m venv .venv source .venv/bin/activate

4.  Install dependencies: pip install -r requirements.txt

5.  Create a .env file in the project root. Do not commit this file to
    Git. Add the environment variables required by config/settings.py,
    including:

    SECRET_KEY= DEBUG=True ALLOWED_HOSTS=127.0.0.1,localhost
    DATABASE_URL=

    Add any other variables referenced by config/settings.py. For a
    local development environment, configure the database and security
    settings appropriately. Do not copy production-only security values
    blindly into a local environment.

6.  Apply database migrations: python manage.py migrate

7.  Start the development server: python manage.py runserver

8.  Open the API in your browser: http://127.0.0.1:8000/

    The root URL may not have a page configured. Use the API routes
    defined in config/urls.py and core/urls.py.

API Documentation

The project uses drf-spectacular for API schema and Swagger
documentation. When the development server is running, the Swagger UI is
expected at:

http://127.0.0.1:8000/api/docs/

If the route differs in the current code, check config/urls.py.

Authentication

The API uses JWT authentication with Django REST Framework and Simple
JWT. Obtain a token using the token endpoints configured in the
project’s URL configuration, then send the access token in requests
using this header:

Authorization: Bearer

The exact token endpoint paths should be checked in config/urls.py.

Testing

Run the project’s tests with:

python manage.py test core

Tests cover key product API behaviors, including listing, creation,
invalid data, unauthenticated access, ownership/permissions, partial
updates, and deletion. The current test count previously reached eight
passing tests; run the command again to confirm the current state.

Database

The project is configured to read the database connection from the
DATABASE_URL environment variable using dj-database-url. A PostgreSQL
database such as Neon can be used. Keep database credentials out of
source code and version control.

Static Files and Production Preparation

The project includes Gunicorn and WhiteNoise configuration and defines
STATIC_ROOT for collected static files. The build.sh script runs:

python manage.py collectstatic –no-input python manage.py migrate

Production deployment still requires setting the correct environment
variables, allowed host name, HTTPS/security settings, and database URL
on the hosting platform. Deployment has not been confirmed as completed.

Security Notes

-   Never commit .env files, SECRET_KEY values, database passwords, or
    tokens.
-   Keep DEBUG=False in production.
-   Set ALLOWED_HOSTS to the actual deployed hostname.
-   Enable HTTPS and production cookie/security settings when supported
    by the hosting environment.
-   Review deployment logs and run Django’s deployment checks before
    release.

Developer Notes

-   Review config/settings.py for all required environment variables.
-   Review config/urls.py and core/urls.py for exact endpoint paths.
-   Keep requirements.txt updated when dependencies change: pip freeze >
    requirements.txt
-   Run tests after changing models, serializers, views, permissions, or
    URLs.
-   Use Git commits with clear, descriptive messages.

License

No license information was provided. Add a LICENSE file if you intend to
publish or distribute this project under a specific license.
