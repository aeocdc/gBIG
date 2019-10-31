# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
'''
Created on Aug 28, 2017
Modified on Aug 28, 2017
@author: Huang Teng
@summary: 
'''
#Join component sequence to a complete sequence
def joinSequence(assembleComponentList):
    wholeSequence=""
    length=len(assembleComponentList)
    for component in assembleComponentList:
        wholeSequence+=component["sequence"]
    
    return wholeSequence
