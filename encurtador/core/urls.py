from django.conf.urls import url, patterns


urlpatterns = patterns('core.views',
    url(r'^listar/urls', 'listar_urls', name='listar'),
    url(r'^registrar/', 'registrar', name='registrar'),
    url(r'^$', 'encurtar_url', name='encurtar'),
    url(r'^(?P<token>[\w=]{0,50})', 'redirecionar_urls', name='redirecionar'),
)
