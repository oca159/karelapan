from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('apps.sitio.urls')),
    url(r'^api/', include('apps.api.urls')),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'^karelecatl/', include('apps.karelecatl.urls')),
    url(r'^material/', include('apps.libro.urls')),
    url(r'^channel.html', 'apps.sitio.views.channel'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^404/$', 'apps.sitio.views.error404'),
        url(r'^403/$', 'apps.sitio.views.error403'),
        url(r'^500/$', 'apps.sitio.views.error500'),
    )

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    import debug_toolbar

    urlpatterns += patterns('',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
