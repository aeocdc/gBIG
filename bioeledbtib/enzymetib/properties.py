#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: properties for enzymetib
'''
import os.path

appName='enzymetib'

#html folder path
htmlFolderPath=appName+'/'

#static folder path
#staticFolderPath=os.path.join(PUBLIC_DIR4Ecoin, 'static').replace('\\', '/')

#media folder path
#mediaFolderPath=os.path.join(PUBLIC_DIR4Ecoin, 'media').replace('\\', '/')

#example folder path
#exampleFolderPath=os.path.join(PUBLIC_DIR4Ecoin,'example').replace('\\','/')

#email host
from_email = 'huang_t@tib.cas.cn'

#database
dbProperties={"dbHost":"localhost",
              "dbUser":"webservice",
              "dbPw":"webservice@web",
              "dbName":"enzymetib",
              "dbUser_test":"huangteng",
              "dbPw_test":"ht@use",}
