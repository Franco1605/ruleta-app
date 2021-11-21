release: python manage.py migrate --no-input
web: gunicorn ruleta.wsgi
main_worker: celery -A ruleta worker --beat --loglevel=info