release: python manage.py migrate --no-input
web: gunicorn ruleta.wsgi
main_worker: python manage.py celery worker --beat --loglevel=info