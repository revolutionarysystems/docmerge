from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dash, name='dash'),
    url(r'^test/$', views.test, name='test'),
]