# -*- coding:utf-8 -*-
import os.path
import uuid
from django.http import HttpResponse
from django.core.servers.basehttp import FileWrapper

from componenttib.properties import *

            
#Handle upload file
def uploadFile(uploadedFile, saveFolder, preName="upload"):
    #saved file name
    savedFileName=preName+"-"+uploadedFile.name
    #backup savedFileName=preName+"-"+str(uuid.uuid1())+os.path.splitext(uploadedFile.name)[1]
    savedFilePath=os.path.join(saveFolder, savedFileName).replace('\\', '/')#saved file path
    pattern="wb+"#write pattern
    
    #print "\nfileTransfer.py 'savedFileName' type:\t"+str(type(savedFileName))+"\n"
    
    destination=open(savedFilePath, pattern)#open file
    for chunk in uploadedFile.chunks():#use chunk to upload file
        destination.write(chunk)#write file
    destination.close()#close file
    
    return savedFilePath


#Handle donwload file
def downloadFile(downloadedFilePath,preName="download"):
    
    #print downloadedFileName
    #print downloadedFilePath
    #print os.path.exists(downloadedFilePath)
    #print os.path.exists(os.path.join(PUBLIC_DIR,"fba",downloadedFolderName).replace('\\', '/'))
    #assert False
    
    wrapper=FileWrapper(file(downloadedFilePath))
    response = HttpResponse(wrapper,content_type="application/octet-stream")
    response['Content-Length']=os.path.getsize(downloadedFilePath)    
    
    response['Content-disposition']='attachment; filename=%s'%(preName+"-"+(os.path.split(downloadedFilePath)[1]))
    #response['Content-disposition']='attachment; filename=%s'%(preName+"-"+fileType+os.path.splitext(os.path.splitext(downloadedFileName)[0])[1]+os.path.splitext(downloadedFileName)[1])
    #response['Content-disposition']='attachment; filename=%s'%(preName+"-"+fileType+os.path.splitext(downloadedFileName)[1])
    #response['Content-disposition']='attachment; filename=%s'%(downloadedFolderName+"-"+preName+"-"+fileType+os.path.splitext(downloadedFileName)[1])
    
    return response


#Save file
def saveFile(savedData,fileFormat="txt", preName="save"):
    #if fileFormat=="txt":
    #saved file name
    savedFileName=preName+"-"+str(uuid.uuid1())+"."+fileFormat
    savedFilePath=os.path.join(mediaFolderPath, savedFileName).replace('\\', '/')#saved file path
    with open(savedFilePath, mode='wb') as savedFile:
        savedFile.writelines(savedData)    
    
    return savedFilePath
