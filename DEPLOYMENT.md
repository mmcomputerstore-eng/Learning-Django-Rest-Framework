# Django REST Framework Deployment Checklist

## 1. Security
- [ ] Set `DEBUG=False` in production.
- [ ] Store a strong, unique `SECRET_KEY` in an environment variable.
- [ ] Add the production domain to `ALLOWED_HOSTS`.
- [ ] Keep `.env` out of Git commits.
- [ ] Store database credentials securely.
- [ ] Confirm that secrets have not been exposed in screenshots, logs, or a public repository.

## 2. HTTPS
- [ ] Configure HTTPS for the production domain.
- [ ] Enable `SECURE_SSL_REDIRECT=True` only after HTTPS is working correctly.
- [ ] Set `SESSION_COOKIE_SECURE=True` for HTTPS deployments.
- [ ] Set `CSRF_COOKIE_SECURE=True` for HTTPS deployments.
- [ ] Configure HSTS only after confirming the site is served entirely over HTTPS.

## 3. Database
- [ ] Configure the production PostgreSQL database using environment variables.
- [ ] Confirm database permissions and connectivity.
- [ ] Run `python manage.py migrate`.
- [ ] Verify that required data is available in the production database.

## 4. Static Files
- [ ] Configure `STATIC_ROOT`.
- [ ] Configure WhiteNoise or another suitable static-file serving solution.
- [ ] Run `python manage.py collectstatic --noinput`.
- [ ] Verify that the admin site and other required static assets load correctly.

## 5. Application Server
- [ ] Confirm that Gunicorn is installed and listed in `requirements.txt`.
- [ ] Start the application with the correct WSGI module, for example:
  `gunicorn config.wsgi:application`
- [ ] Configure the hosting platform to run the application with the required port and settings.
- [ ] Check application logs for startup errors.

## 6. API and Tests
- [ ] Run `python manage.py check`.
- [ ] Run `python manage.py test core`.
- [ ] Test JWT authentication.
- [ ] Test product listing, creation, retrieval, updates, deletion, and stock actions.
- [ ] Verify permissions, filtering, searching, ordering, and pagination.
- [ ] Verify the API documentation endpoint, such as `/api/docs/`.

## 7. Final Production Checks
- [ ] Confirm that `DEBUG` is `False`.
- [ ] Confirm that `ALLOWED_HOSTS` contains only the intended hosts.
- [ ] Run `python manage.py check --deploy` and review all remaining warnings.
- [ ] Confirm that `.env`, database files, backups, and secrets are not committed to Git.
- [ ] Test the deployed API over HTTPS.