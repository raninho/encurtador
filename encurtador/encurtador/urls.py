from django.conf.urls import patterns, url, include
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = patterns('',
    url(r'^login', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^logout', 'django.contrib.auth.views.logout_then_login', {'login_url': '/login/'}, name='logout'),
    url(r'^', include('core.urls', namespace='core', app_name='core')),
)

urlpatterns += staticfiles_urlpatterns()
