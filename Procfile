release: python manage.py migrate --no-input
web: gunicorn ruleta.wsgi
worker: celery -A ruleta worker -l info
beat: celery -A ruleta beat -l info