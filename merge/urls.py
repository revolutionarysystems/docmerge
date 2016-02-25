from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^merge/', views.merge, name='merge'),
]