from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^merge/', views.merge, name='merge'),
    url(r'^merge-get/', views.merge_get, name='merge_get'),
    url(r'^file/', views.file, name='file'),
]