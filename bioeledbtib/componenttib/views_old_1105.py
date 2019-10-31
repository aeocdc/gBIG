# -*- coding:utf-8 -*-
'''
Created on 20170303
@author: Huang Teng
@summary: views for componenttib
'''
# Create your views here.
from django.shortcuts import render,render_to_response
from django.http import HttpResponse
from django.template import RequestContext

from django.core.mail import EmailMultiAlternatives

from properties import htmlFolderPath,appName,from_email
from util.fileTransfer import uploadFile

import os

import logging
#backup 无效 logging.basicConfig(level=logging.DEBUG)#temp log
logger = logging.getLogger("developing")#debug log
#logger = logging.getLogger(__name__)

#database
def selectData(tableName,fieldNameArray,parameterDic):
    #prepare db
    import util.dbOperator as dbor
    dbConn,dbCursor=dbor.prepareDb()
    
    #fetch data
    sqlString="select distinct "+(",".join(fieldNameArray))+" from "+tableName
    if (parameterDic):
        parameterData=[]
        parameterTitle=[]
        for k,v in parameterDic.iteritems():
            parameterData.append(v)
            parameterTitle.append(k)
        sqlString=sqlString+" where ("+(",".join(parameterTitle))+")=('"+("','".join(parameterData))+"')"
#     logger.debug(sqlString)
    
    sqlResultData,sqlResultCount=dbor.sqlSelect(sqlString,dbCursor)
#     logger.debug(sqlResultCount)
    #close
    dbConn.close()
    return sqlResultData,sqlResultCount

#template mange           
def htmlPage(queryName,):
    htmlDict={"component5Design":"component5Design","designModule":"assembleSequence","sendAssemble":"httpString","sgrna5Design":"httpString",}
    inputHtmlPath=os.path.join(htmlFolderPath, queryName+'.html').replace('\\', '/')
    resultHtmlPath=os.path.join(htmlFolderPath,htmlDict[queryName]+'.html').replace('\\', '/')
    return inputHtmlPath,resultHtmlPath

def sgrna(request,queryName="sgrna5Design"):
    inputHtmlPath,resultHtmlPath=htmlPage(queryName)
    from forms import formDict# 引入我们创建的表单类
    if request.method != 'POST':# 当正常访问时
        if queryName=="sgrna5Design":
            form = formDict[queryName]()
    else:# 当提交表单时
        form=formDict[queryName](request.POST,request.FILES)
        if form.is_valid():# 如果提交的数据合法
            formData=form.cleaned_data
            
            if queryName=="sgrna5Design":
                #dtgeneSequence=formData["dtgeneSequence"]
                geneFile8Upload=formData["geneFile8Upload"]
                referenceFile8Upload=formData["referenceFile8Upload"]
                userEmail=formData["userEmail"]
                
                from userManage import taskSpaceCheck
                taskSpacePath,userSpacePath,userTrackFilePath=taskSpaceCheck(userEmail.split("@")[0],queryName)#task space
                geneFilePath=uploadFile(uploadedFile=geneFile8Upload,saveFolder=taskSpacePath,preName="geneFile")#upload and save file
                referenceFilePath=uploadFile(uploadedFile=referenceFile8Upload,saveFolder=taskSpacePath,preName="referenceFile")#upload and save file
                #design sgrna
                from func.designSgrna import sgrnacas9
                sgrna_reportFilePath=sgrnacas9(taskSpacePath,geneFilePath,referenceFilePath)
                
                #session
                request.session["geneFilePath"] =geneFilePath
                request.session["referenceFilePath"]=referenceFilePath
                #request.session["dtgeneSequence"]=dtgeneSequence
                request.session["userEmail"]=userEmail
                request.session["sgrna_reportFilePath"]=sgrna_reportFilePath
                #email
                wetlab_email='spacewalkerht@163.com'
                subject="SgRNA"
                content="SgRNA\n"
                content+="Target gene file is "+geneFile8Upload.name+"\n"
                content+="Reference genome file is "+referenceFile8Upload.name+"\n"
                content+="Please see the attached sgRNA files."
                msg=EmailMultiAlternatives('sgRNA',content,from_email,[wetlab_email,userEmail,])
                msg.attach_file(sgrna_reportFilePath)
                msg.send()
                
                httpString="<div><h3>Desgin sgRNA for target gene inactivation</h3></div>\
                            <div><p>Target gene file is <br/>"+geneFile8Upload.name+"</p>\
                                <p>Reference genome file is <br/>"+referenceFile8Upload.name+"</p>\
                                <p>SgRNA will be sent to "+userEmail+"</p>\
                                <p>Please contact to <a href\""+wetlab_email+"\">"+wetlab_email+"</a> for wet-lab technical support and "+"<a href\"huang_t@tib.cas.cn\">Teng Huang</a>"+" for computing-lab technical support</p></div>"
                #backup
                #symbolList=symbol.split(",")
            #calculate success, direct to the result page
            return render(request,resultHtmlPath,locals())
    return render(request,inputHtmlPath,locals())

def assemble(request,queryName="component5Design"):
    inputHtmlPath,resultHtmlPath=htmlPage(queryName)
    from forms import formDict# 引入我们创建的表单类
    if request.method != 'POST':# 当正常访问时
        if queryName=="component5Design":
            organismList=["E.coli","S.cerevisiae","C.glutamicum",]
            navL1LinkList=[]
            from models import NavLink
            for organism in organismList:
                navL1LinkList.append(NavLink(organism,""))
        #backup
        #form = formDict[queryName]()
    else:# 当提交表单时
        form=formDict[queryName](request.POST,request.FILES)
        if form.is_valid():# 如果提交的数据合法
            formData=form.cleaned_data
            
            if queryName=="designModule":
                assembleComponentList=request.POST.get("assembleComponentList")
                len_ha=request.POST.get("len_ha")
                len_ha=int(len_ha) if len_ha else 20
                
                import util.dataEncapsulater as deer
                #design primer
                from func.designPrimer import primerList
                assembleComponentListDict=deer.decapsulateJson(assembleComponentList)
                primerDataListDict=primerList(assembleComponentListDict,len_ha)
                primerDataList=deer.encapsulateJson(primerDataListDict)
                #join assembleComponent
#                 from func.joinComponent import joinSequence
#                 wholeSequence=joinSequence(assembleComponentListDict)
                request.session["assembleComponentList"]=assembleComponentList
                request.session["len_ha"]=len_ha
                request.session["primerDataList"]=primerDataList
                
            if queryName=="sendAssemble":
                #store user_submit
                #prepare db
                import util.dbOperator as dbor
                dbConn,dbCursor=dbor.prepareDb()
                #store
                sqlString="insert into user_submit (assembleComponentList,len_ha,submit_time) values (\'"+request.session["assembleComponentList"]+"\',"+str(request.session["len_ha"])+",now())"
                #backup 存的是单引号且字典内部顺序非原始 sqlString="insert into test (assembleComponentList,submit_time) values (\""+str(assembleComponentListDict)+"\",now())"
                isContinue=dbor.sqlDo(sqlString,dbCursor,dbConn)
                if(not isContinue):
                    logger.warning(sqlString)
                #close
                dbConn.close()
                #email assemble list
                wetlab_email='spacewalkerht@163.com'
                subject="Assemble component"
                content="Assemble Component\n"
                content+="Assemble Component List: \n"+request.session["assembleComponentList"]+"\n"
                content+="Primer Data List: \n"+request.session["primerDataList"]+"\n"
                content+="Length of homologous arm: \n"+str(request.session["len_ha"])+"\n"
                msg=EmailMultiAlternatives(subject,content,from_email,[wetlab_email,])
                msg.send()
                
                httpString="<div><h3>Design biocomponent</h3></div>\
                            <div><p>Task has been sent to laboratory</p>\
                                <p>Please contact to <a href\""+wetlab_email+"\">"+wetlab_email+"</a> for wet-lab technical support and "+"<a href\"huang_t@tib.cas.cn\">Teng Huang</a>"+" for computing-lab technical support</p></div>"
                
                
                #backup
                #symbolList=symbol.split(",")
            #calculate success, direct to the result page
            return render(request,resultHtmlPath,locals())
    #form = formDict[queryName]()
    return render(request,inputHtmlPath,locals())
'''backup
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
    return render(request,resultHtmlPath,locals())'''

def componentList(request,organism,**kargs):
    import util.dataEncapsulater as deer
    if not (kargs):
        componentTypeList=["promoter","promoter_function_module","terminator","terminator_function_module","replication_origin","replication_origin_function_module","selection_marker","selection_marker_function_module"]
        from models import NavLink
        import collections
        resultDataDict=collections.OrderedDict()
        for componentType in componentTypeList:
            resultDataDict[componentType]=NavLink(organism,componentType).get_absolute_url()
        resultDataJson=deer.encapsulateJson(resultDataDict)
    else:
        componentType=kargs["componentType"]
        fieldNameData,fieldNameCount=selectData("information_schema.columns",["COLUMN_NAME"],{"table_name":componentType})
        if(fieldNameCount>0):
           resultTitle=[inner_1[0] for inner_1 in fieldNameData][1:]
           resultData,resultCount=selectData(componentType,resultTitle,{"organism":organism})
           resultDataDict=deer.encapsulateDict(resultTitle,resultData)
           resultDataJson=deer.encapsulateJson(resultDataDict)
        #backup
        #resultTypeDic={}
           #backup
           #resultTypeDic[resultType]={"resultTitle":resultTitle,
           #                           "resultCount":resultCount,
           #                           "resultData":resultData,
           #                           "resultDataDict":resultDataDict,}
    return HttpResponse(resultDataJson)

#index
def index(request):
    #overview
    resultTitle=["enzymeId","substrateName","productName",]
    
    #fetch data
    import MySQLdb
    import util.dbOperator as dbor
    from properties import dbProperties
    dbConn = MySQLdb.connect(host=dbProperties["dbHost"],user=dbProperties["dbUser"],passwd=dbProperties["dbPw"],db="enzymetib",charset='utf8')
    dbCursor = dbConn.cursor()
    
    tableName="enzyme"
    fieldNameArray=resultTitle
    parameterDic={}
    sqlString="select distinct "+(",".join(fieldNameArray))+" from "+tableName
    if (parameterDic):
        parameterData=[]
        parameterTitle=[]
        for k,v in parameterDic.iteritems():
            parameterData.append(v)
            parameterTitle.append(k)
        sqlString=sqlString+" where ("+(",".join(parameterTitle))+")=('"+("','".join(parameterData))+"')"
    #logger.debug(sqlString)
    
    sqlResultData,sqlResultCount=dbor.sqlSelect(sqlString,dbCursor)
    #logger.debug(sqlResultCount)

    dbConn.close()
    #return sqlResultData,sqlResultCount

    resultData,resultCount=sqlResultData,sqlResultCount
    #resultData,resultCount=selectData("enzyme",resultTitle,{})
    
    return render(request, os.path.join(htmlFolderPath,'index.html').replace('\\', '/'),locals())