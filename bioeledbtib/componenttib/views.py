# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 11:55:45 2018

@author: ht
"""

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
    htmlDict={"component5Design":"component5Design","designModule":"assembleSequence","sendAssemble":"httpString","gBIG":"httpString","gBIG_help":"httpString"}
    inputHtmlPath=os.path.join(htmlFolderPath, queryName+'.html').replace('\\', '/')
    resultHtmlPath=os.path.join(htmlFolderPath,htmlDict[queryName]+'.html').replace('\\', '/')
    return inputHtmlPath,resultHtmlPath

def sgrna(request,queryName="gBIG"):
    inputHtmlPath,resultHtmlPath=htmlPage(queryName)
    from forms import formDict# 引入我们创建的表单类
    if request.method != 'POST':# 当正常访问时
        if queryName=="gBIG":
            form = formDict[queryName]()
    else:# 当提交表单时
        form=formDict[queryName](request.POST,request.FILES)
        if form.is_valid():# 如果提交的数据合法
            formData=form.cleaned_data

            if queryName=="gBIG":
                pam_value=request.POST.get("pam_type")
                if pam_value=='sgRNAcas9-NAG':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NAG.pl"
                elif pam_value=='sgRNAcas9-NGA':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NGA.pl"
                elif pam_value=='sgRNAcas9-NGCG':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NGCG.pl"
                elif pam_value=='sgRNAcas9-NGG':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NGG.pl"
                elif pam_value=='sgRNAcas9-NGN':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NGN.pl"
                elif pam_value=='sgRNAcas9-NGT':
                    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/sgRNAcas9-NGT.pl"

                geneFile8Upload=formData["geneFile8Upload"]
                userEmail=formData["userEmail"]
                #
                #referenceFilePath="/home/webservice/bioeledbtib/componenttib/media/410499871/5d574989-eec2-5f12-88d7-61f2bc359dbb/referenceFile-ATCC13032-reference genome"
                from userManage import taskSpaceCheck
                taskSpacePath,userSpacePath,userTrackFilePath=taskSpaceCheck(userEmail.split("@")[0],queryName)#task space
                geneFilePath=uploadFile(uploadedFile=geneFile8Upload,saveFolder=taskSpacePath,preName="geneFile")#upload and save file
                #
                base_editor_value=request.POST.get("base_editor_type")
                if base_editor_value=='Target_AID1':
                    nxmAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/check_sgRNA_C_AID.pl"
                elif base_editor_value=='BE2':
                    nxmAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/New_pl/check_sgRNA_C_BE.pl"
                #
                modelUseType=formData["modelUseType"]
                if(modelUseType=="select"):
                    ref_value=request.POST.get("ref_seq")
                    if ref_value=='ASM584v2':
                        referenceFilePath="/home/webservice/ref/ASM584v2.fna"
                        refname='ASM584v2'
                    elif ref_value=='ASM1132v1':
                        referenceFilePath="/home/webservice/ref/ASM1132v1.fna"
                        refname='ASM1132v1'
                    elif ref_value=='ASM904v1':
                        referenceFilePath="/home/webservice/ref/ASM904v1.fna"
                        refname='ASM904v1'
                    elif ref_value=='NC_001136.10':
                        referenceFilePath="/home/webservice/ref/NC_001136.10.fna"
                        refname='NC_001136.10'
                    elif ref_value=='GRCm38.p6':
                        referenceFilePath="/home/webservice/ref/GRCm38.p6.fna"
                        refname='GRCm38.p6'
                    elif ref_value=='GRCh38.p12':
                        referenceFilePath="/home/webservice/ref/GRCh38.p12.fna"
                        refname='GRCh38.p12'
                    elif ref_value=='hs_ref_GRCh38.p12_chr1':
                        referenceFilePath="/home/webservice/ref/hs_ref_GRCh38.p12_chr1.fna"
                        refname='hs_ref_GRCh38.p12_chr1'

                elif(modelUseType=="upload"):
                    referenceFile8Upload=formData["referenceFile8Upload"]
                    referenceFilePath=uploadFile(uploadedFile=referenceFile8Upload,saveFolder=taskSpacePath,preName="referenceFile")#upload and save file
                    refname=referenceFile8Upload.name
                #return web page information
                wetlab_email='aeocdctibcas@163.com'
                httpString="<div><h3>Desgin sgRNA for target gene inactivation</h3></div>\
                            <div><p>PAM type is <br/>"+pam_value+"</p>\
                                <p>Base editor type is <br/>"+base_editor_value+"</p>\
                                <p>Target gene file is <br/>"+geneFile8Upload.name+"</p>\
                                <p>Reference genome file is <br/>"+refname+"</p>\
                                <p>SgRNA will be sent to "+userEmail+"</p>\
                                <p>Please contact to <a href\""+wetlab_email+"\">"+wetlab_email+"</a> for wet-lab technical support and "+"<a href\"aeocdctibcas@163.com\">Yi Yang</a>"+" for computing-lab technical support</p></div>"

                #dtgeneSequence=formData["dtgeneSequence"])
                #design sgrna
                from func.designSgrna import sgrnacas9
                sgrna_reportFilePath=sgrnacas9(taskSpacePath,geneFilePath,referenceFilePath,sgrnaAppFilePath,nxmAppFilePath,pam_value)
                #session
                request.session["PAM_Type"] =pam_value
                request.session["geneFilePath"] =geneFilePath
                request.session["referenceFilePath"]=referenceFilePath
                #request.session["dtgeneSequence"]=dtgeneSequence
                request.session["userEmail"]=userEmail
                request.session["sgrna_reportFilePath"]=sgrna_reportFilePath
                #email
                wetlab_email='aeocdctibcas@163.com'
                subject="SgRNA"
                content="SgRNA\n"
                content+="PAM type is "+pam_value+"\n"
                content+="Base editor type is "+base_editor_value+"\n"
                content+="Target gene file is "+geneFile8Upload.name+"\n"
                content+="Reference genome file is "+refname+"\n"
                content+="Please see the attached sgRNA files."+"\n"
                msg=EmailMultiAlternatives('sgRNA',content,from_email,[wetlab_email,userEmail,])
                msg.attach_file(sgrna_reportFilePath)
                msg.send()

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
                wetlab_email='aeocdctibcas@163.com'
                subject="Assemble component"
                content="Assemble Component\n"
                content+="Assemble Component List: \n"+request.session["assembleComponentList"]+"\n"
                content+="Primer Data List: \n"+request.session["primerDataList"]+"\n"
                content+="Length of homologous arm: \n"+str(request.session["len_ha"])+"\n"
                msg=EmailMultiAlternatives(subject,content,from_email,[wetlab_email,])
                msg.send()

                httpString="<div><h3>Design biocomponent</h3></div>\
                            <div><p>Task has been sent to laboratory</p>\
                                <p>Please contact to <a href\""+wetlab_email+"\">"+wetlab_email+"</a> for wet-lab technical support and "+"<a href\"aeocdctibcas@163.com\">Yi Yang</a>"+" for computing-lab technical support</p></div>"


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

'''#index
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

    return render(request, os.path.join(htmlFolderPath,'index.html').replace('\\', '/'),locals())'''

def gBIG_help(request):
    return render(request, "gBIG_help.html")
