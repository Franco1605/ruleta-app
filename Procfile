release: python manage.py migrate --no-input
web: gunicorn djangoherokuapp.wsgi --log-file -
celery: celery -A ruleta worker -l info
celery: celery -A ruleta beat -l info