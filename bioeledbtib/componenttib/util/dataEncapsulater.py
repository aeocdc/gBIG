# -*- coding:utf-8 -*-
'''
Created on 20170502
@author: Huang Teng
'''
def encapsulateDict(title,data,**kargs):
    skipIndex=[]
    if(kargs):
        for k,v in kargs.iteritems():
            skipIndex.append(v)
    
    import collections
    dataDict=[]
    for dataLine in data:
        fieldDict=collections.OrderedDict()
        if(kargs):
            for k,v in kargs.iteritems():
                fieldDict[k]=dataLine[v]
        #fieldDict["source"]=dataLine[0]
        #fieldDict["type"]="noma"
        for index4F,field in enumerate(dataLine):
            if index4F not in skipIndex:
                fieldDict[title[index4F]]=dataLine[index4F]
        dataDict.append(fieldDict)
    return dataDict
        
def encapsulateJson(dataDict):
    import json
    dataJson=json.dumps(dataDict)
    return dataJson
def decapsulateJson(dataJson):
    import json
    dataDict=json.loads(dataJson)
    return dataDict

