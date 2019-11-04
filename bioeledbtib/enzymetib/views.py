#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: views for enzymetib
'''
# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from properties import htmlFolderPath,appName

import os

import logging
#backup 无效 logging.basicConfig(level=logging.DEBUG)#temp log
logger = logging.getLogger("developing")#debug log
#logger = logging.getLogger(__name__)


def htmlPage():
    inputHtmlPath=os.path.join(htmlFolderPath,'Input.html').replace('\\', '/')
    resultHtmlPath=os.path.join(htmlFolderPath,'Result.html').replace('\\', '/')
    return inputHtmlPath,resultHtmlPath
    
def selectData(tableName,fieldNameArray,parameterDic):
    #fetch data
    import MySQLdb
    import dbOperator as dbor
    from properties import dbProperties
    dbConn = MySQLdb.connect(host=dbProperties["dbHost"],user=dbProperties["dbUser_test"],passwd=dbProperties["dbPw_test"],db=dbProperties["dbName"],charset='utf8')
    dbCursor = dbConn.cursor()
    
    sqlString="select distinct "+(",".join(fieldNameArray))+" from "+tableName
    if (parameterDic):
        parameterData=[]
        parameterTitle=[]
        for k,v in parameterDic.iteritems():
            parameterData.append(v)
            parameterTitle.append(k)
        sqlString=sqlString+" where ("+(",".join(parameterTitle))+")=('"+("','".join(parameterData))+"')"
    logger.debug(sqlString)
    
    sqlResultData,sqlResultCount=dbor.sqlSelect(sqlString,dbCursor)
    logger.debug(sqlResultCount)

    dbConn.close()
    '''#backup for json
    sqlResultDataDict=[]
    for dataLine in sqlResultData:
        fieldDict=collections.OrderedDict()
        fieldDict["source"]=dataLine[0]
        fieldDict["target"]=dataLine[1]
        fieldDict["type"]="noma"
        for index4F,field in enumerate(dataLine):
            if index4F not in [0,1]:
                fieldDict[sqlResult1Title[index4F]]=dataLine[index4F]
        sqlResultDataDict.append(fieldDict)
    sqlResultData4Json=json.dumps(sqlResultDataDict)'''
    return sqlResultData,sqlResultCount

def search(request,):
    queryName="search"
    inputHtmlPath,resultHtmlPath=htmlPage()
    from forms import formDict# 引入我们创建的表单类
    if request.method == 'POST':# 当提交表单时
        form=formDict[queryName](request.POST,request.FILES)
        if form.is_valid():# 如果提交的数据合法
            formData=form.cleaned_data
            symbolType = formData["symbolType"]
            symbolValue = formData["symbolValue"]
            
            resultTitle=["enzymeId","substrateName","productName",]
            parameterDic={symbolType:symbolValue}
            resultData,resultCount=selectData("enzyme",resultTitle,parameterDic)
            if (resultCount):
                logger.debug(resultData[0][1])
            #calculate success, direct to the result page
            return render(request,resultHtmlPath,locals())
    else:# 当正常访问时
        form = formDict[queryName]()
    return render(request,inputHtmlPath,locals())
  
def search8Url(request,symbolType="enzymeId",symbolValue="KRED027"):
    symbolTypeListArray=["enzymeId","substrateName","productName",]
    if symbolType not in symbolTypeListArray:
        return HttpResponse("Invalid symbol Type.")
    queryName="search"
    inputHtmlPath,resultHtmlPath=htmlPage()
    
    resultTitle=["enzymeId","substrateName","productName",]
    parameterDic={symbolType:symbolValue}
    resultData,resultCount=selectData("enzyme",resultTitle,parameterDic)
    
    #calculate success, direct to the result page
    return render(request,resultHtmlPath,locals())

'''#backup 多参数方式，未完成
def search8Url(request,queryParameterString="enzymeId*KRED027#"):
    symbolType="enzymeId",symbolValue="KRED027"
    
    queryParameterData=[[("\N" if str(inner_2[1:-1])=="" else str(inner_2[1:-1])) for inner_2 in re.findall(r'\*.*?#',inner_1)] for inner_1 in brendaResultTemp]
    queryParameterTitle=[re.search(r'[^\*#]+', inner_1).group() for inner_1 in re.findall(r'#.+?\*|^.+?\*',brendaResultTemp[0])]
'''    

#index
def index(request):
    #overview
    resultTitle=["enzymeId","substrateName","productName",]
    resultData,resultCount=selectData("enzyme",resultTitle,{})
    
    return render(request, os.path.join(htmlFolderPath,'index.html').replace('\\', '/'),locals())