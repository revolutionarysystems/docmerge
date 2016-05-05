from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^merge/', views.merge, name='merge'),
    url(r'^push/', views.push, name='push'),
    url(r'^merge-get/', views.merge_get, name='merge_get'),
    url(r'^file/', views.file, name='file'),
    url(r'^refresh/', views.refresh, name='refresh'),
    url(r'^zip/', views.zip, name='zip'),
    url(r'^upload-zip/$', views.upload_zip, name='upload_zip'),
    url(r'^download-zip/$', views.download_zip, name='download_zip'),
]