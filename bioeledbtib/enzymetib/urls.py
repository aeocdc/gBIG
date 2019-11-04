#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: urls for enzymetib
'''
from django.conf.urls import patterns, include, url
import os
from enzymetib import views as enzymetib_views
from bioeledbtib.settings import BASE_DIR4enzymetib

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(BASE_DIR4enzymetib, 'static').replace('\\', '/')}),
    
    url(r'^search/$',enzymetib_views.search, name='search4enzymetib'),
    url(r'^search/(?P<symbolType>\w+)/(?P<symbolValue>\w+)/$','enzymetib.views.search8Url', name='search8Url4enzymetib'),
    url(r'^$','enzymetib.views.index'),
    
)

