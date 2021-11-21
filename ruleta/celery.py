from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE','ruleta.settings')
app = Celery('ruleta')

app.config_from_object('django.conf:settings')

app.conf.beat_schedule = {
    'every-3-minutes':{
        'task':'ruleta_app.tasks.ruleta',
        'schedule': 180,
    },
    'at-end-day':{
        'task':'ruleta_app.tasks.reponer_dinero',
        'schedule': crontab(hour=0, minute=00),
    }
    
}

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))