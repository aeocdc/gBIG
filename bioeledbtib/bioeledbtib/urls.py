#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: urls for bioeledbtib
'''
from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    # url(r'^$', 'bioeledbtib.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    
    url(r'^enzymetib/', include('enzymetib.urls')),
    url(r'^componenttib/', include('componenttib.urls')),
    
    url(r'^admin/', include(admin.site.urls)),
]
