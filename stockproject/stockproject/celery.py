from __future__ import absolute_import, unicode_literals
import os
from  celery import Celery
from django.conf import settings
# from celery.schedules import crontab # crontab - allocating periodic tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')

app = Celery('stockproject')
app.conf.enable_utc = False
app.conf.update(timezone='Asia/Kolkata')    

app.config_from_object(settings, namespace='CELERY')

app.conf.beat_schedule = {
    # 'every-10-seconds': {
    #     'task': 'mainapp.tasks.update_stock',  # Corrected task path
    #     'schedule': 10.0,
    #     'args': (['RELIANCE.NS', 'TCS.NS'],)  # Correct tuple format
    # }
}

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')




# from __future__ import absolute_import, unicode_literals
# import os
# from celery import Celery
# from django.conf import settings
# import logging

# logger = logging.getLogger(__name__)

# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stockproject.settings')

# app = Celery('stockproject')
# app.conf.enable_utc = False
# app.conf.update(timezone='Asia/Kolkata')

# app.config_from_object('django.conf:settings', namespace='CELERY')

# app.conf.beat_schedule = {
#     # 'every-10-seconds': {
#     #     'task': 'mainapp.tasks.update_stock',  # Corrected task path
#     #     'schedule': 10.0,
#     #     'args': (['RELIANCE.NS', 'TCS.NS'],)  # Correct tuple format
#     # }
# }

# app.conf.beat_scheduler = 'django_celery_beat.schedulers:DatabaseScheduler'

# app.autodiscover_tasks()

# @app.task(bind=True)
# def debug_task(self):
#     print(f'Request: {self.request!r}')

# logger.info("Celery Beat Schedule: %s", app.conf.beat_schedule)