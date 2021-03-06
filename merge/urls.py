from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^merge/', views.merge, name='merge'),
    url(r'^bulk_merge/', views.bulk_merge, name='bulk_merge'),
    url(r'^push/', views.push, name='push'),
    url(r'^merge-get/', views.merge_get, name='merge_get'),
    url(r'^file/link/', views.file_link, name='file_link'),
    url(r'^file/', views.file, name='file'),
    url(r'^refresh/', views.refresh, name='refresh'),
    url(r'^cull/', views.cull_outputs, name='cull'),
    url(r'^clear/', views.clear_resources, name='clear'),
    url(r'^delete/$', views.delete, name='delete'),
    url(r'^zip/', views.zip_files, name='zip'),
    url(r'^upload-zip/$', views.upload_zip, name='upload_zip'),
    url(r'^patch-zip/$', views.patch_zip, name='patch_zip'),
    url(r'^download-zip/$', views.download_zip, name='download_zip'),
    url(r'^ajax/compose-preview/$', views.compose_preview, name='compose_preview'),
    url(r'^ajax/sample-data/$', views.sample_data, name='sample_data'),
    url(r'^ajax/styling/$', views.styling, name='styling'),
    url(r'^ajax/change-folder/$', views.change_folder, name='change_folder'),
    url(r'^ajax/load-template/$', views.load_template, name='load_template'),

]