#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: urls for componenttib
'''
from django.conf.urls import patterns, include, url
import os
from componenttib import views as componenttib_views
from bioeledbtib.settings import BASE_DIR4COMPONENTTIB

urlpatterns = patterns('',
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve',{'document_root':os.path.join(BASE_DIR4COMPONENTTIB, 'static').replace('\\', '/')}),
    
    #url(r'^$',componenttib_views.assemble, name='assemble'),
    url(r'^component/(?P<queryName>\w+)/$',componenttib_views.assemble, name='assemble'),
    url(r'^component/(?P<organism>\w+\.?\w+)/$',componenttib_views.componentList,name='componentList'),
    url(r'^component/(?P<organism>\w+\.?\w+)/(?P<componentType>\w+)/$',componenttib_views.componentList,name='componentList'),
    #url(r'^$',componenttib_views.assemble, name='assemble'),
    
    url(r'^$',componenttib_views.sgrna, name='sgrna'),
    url(r'^sgrna/(?P<queryName>\w+)/$',componenttib_views.sgrna, name='sgrna'),
    #backup url(r'^search/(?P<symbolType>\w+)/(?P<symbolValue>\w+)/$',componenttib_views.search8Url, name='search8Url4componenttib'),
    #url(r'^$',componenttib_views.index),
)

