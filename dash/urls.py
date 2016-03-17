from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dash, name='dash'),
    url(r'^home/$', views.dash, name='home'),
    url(r'^test/$', views.test, name='test'),
    url(r'^test-result/$', views.test_result, name='test_result'),
    url(r'^library/$', views.library, name='library'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^account/$', views.account, name='account'),
    url(r'^links/$', views.links, name='links'),
]