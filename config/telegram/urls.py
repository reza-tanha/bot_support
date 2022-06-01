from django.urls import path
from .views import *

app_name = 'telegram'
urlpatterns = [
    path('', update, name='telegram'),
]
