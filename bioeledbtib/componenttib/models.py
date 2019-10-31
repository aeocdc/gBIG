# -*- coding:utf-8 -*-
'''
Created on 20170623
@author: Huang Teng
'''

class NavLink():
    def __init__(self, organism, componentType):
        self.organism = organism
        self.componentType = componentType
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        if self.componentType == "":
            return reverse('componentList', args=(self.organism,))
        else:
            return reverse('componentList', args=(self.organism, self.componentType,))
    def __unicode__(self):
        return self.componentType
    #backup用于admin
    #class Meta:
    #    ordering = ['componentType']  # 按照哪个排序