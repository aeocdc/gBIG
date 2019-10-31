#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: properties for componenttib
'''
import os.path
from django.conf import settings

appName='componenttib'

#html folder path
htmlFolderPath=appName+'/'

#static folder path
#staticFolderPath=os.path.join(PUBLIC_DIR4Ecoin, 'static').replace('\\', '/')

#media folder path
mediaFolderPath=os.path.join(settings.BASE_DIR4COMPONENTTIB, 'media').replace('\\', '/')

#example folder path
#exampleFolderPath=os.path.join(PUBLIC_DIR4Ecoin,'example').replace('\\','/')

#email host
from_email = settings.DEFAULT_FROM_EMAIL

#database
dbProperties={"dbHost":"localhost",
              "dbUser":"webservice",
              "dbPw":"webservice@web",
              "dbName":"componenttib",
              "dbUser_test":"huangteng",
              "dbPw_test":"ht@use",}
