from __future__ import absolute_import,unicode_literals
import os
from celery import Celery
from django.conf import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "categories_product.settings")

app = Celery('categories_product')
app.conf.enable_utc = False

app.conf.update(timezone = 'Asia/Kolkata')

app.config_from_object(settings,namespace = 'CELERY')

# app.conf.beat_schedule ={
#     "mail_sent_every_2min_after_ApiCall":{
#         "task":"users.tasks.send_delayed_email",
#         "schedule": timedelta(minutes=2)
#     }
# }

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')