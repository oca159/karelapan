# -*- coding: utf-8 -*-
from django.conf.urls import patterns,url, include

urlpatterns = patterns('apps.karelecatl.views',
    url(r'^$', 'inicio'),
)
