from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dash, name='dash'),
    url(r'^home/$', views.dash, name='home'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test-result-get/$', views.test_result_get, name='test_result_get'),
    url(r'^test-result-post/$', views.test_result_post, name='test_result_post'),
    url(r'^library/$', views.library, name='library'),
    url(r'^library_folder/$', views.library_folder, name='library'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^account/$', views.account, name='account'),
    url(r'^links/$', views.links, name='links'),
]