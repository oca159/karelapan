from django.conf.urls import patterns,url

urlpatterns = patterns('apps.api.views',
    url(r'^$', 'index'),
    url(r'^mundo_ejemplo/(?P<id_problema>\d+)/$', 'mundo_ejemplo'),
    url(r'^mundo_ejemplo_solucion/(?P<id_problema>\d+)/$', 'mundo_ejemplo_solucion'),
)