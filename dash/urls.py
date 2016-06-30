from django.conf.urls import url
from django.contrib.auth import views as auth_views
from . import views




url(r'^accounts/login/$', auth_views.login),
 
url(r'^accounts/login/$', auth_views.login),


urlpatterns = [
    url(r'^$', views.dash, name='dash'),
    url(r'^home/$', views.dash, name='home'),
#    url(r'^(?P<shelf>.+)/home/$', views.dash, name='home'),
    url(r'^test/$', views.test, name='test'),
#    url(r'^(?P<shelf>.+)/home/$', views.dash, name='home'),
    url(r'^test-nav/$', views.test, name='test'),
    url(r'^test-result-get/$', views.test_result_get, name='test_result_get'),
    url(r'^test-result-post/$', views.test_result_post, name='test_result_post'),
    url(r'^library/$', views.library, name='library'),
    url(r'^library_folder/$', views.library_folder, name='library_folder'),
    url(r'^link/$', views.library_link, name='library_link'),
    url(r'^archive/$', views.archive, name='archive'),
    url(r'^account/$', views.account, name='account'),
    url(r'^links/$', views.links, name='links'),
    url(r'^accounts/login/$', auth_views.login),
    url(r'^accounts/logout/$', views.logout_view),
 #   url(r'^(?P<shelf>\w+)/$', views.dash, name='dash'),
]