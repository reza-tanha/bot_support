from __future__ import absolute_import
import os
from celery import Celery, Task
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config')

# class MyTask(Task):

#     def __call__(self, *args ,**kwargs):
#         return self.run( *args **kwargs) 

# app.Task = MyTask

app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

    