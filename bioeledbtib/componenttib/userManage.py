# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
'''
Created on Mar 22, 2018
Modified on Mar 22, 2018
@author: Teng Huang
@summary: user manage
'''
from .properties import mediaFolderPath

import os,stat
from datetime import datetime

import logging
#backup 无效 logging.basicConfig(level=logging.DEBUG)#temp log
logger = logging.getLogger("developing")#debug log

#user space
def userSpaceCheck(userSpaceName):
    userSpacePath=os.path.join(mediaFolderPath, userSpaceName).replace('\\', '/')+"/"
    userTrackFilePath=userSpacePath+"userTrack.log"
    if not os.path.exists(userSpacePath):
        os.makedirs(userSpacePath)
        #os.chmod(userSpacePath,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
        with open(userTrackFilePath,"w") as userTrackFile:
            userTrackFile.write(datetime.now().strftime('%d %b %Y %H:%M:%S')+" - Create user space - "+userSpacePath)
    return userSpacePath,userTrackFilePath

#task space
def taskSpaceCheck(userSpaceName,taskName):
    userSpacePath,userTrackFilePath=userSpaceCheck(userSpaceName)#user space
    import uuid
    taskSpaceName=str(uuid.uuid5(uuid.uuid1(), str(taskName)))
    taskSpacePath=os.path.join(userSpacePath, taskSpaceName).replace('\\', '/')+"/"
    if not os.path.exists(taskSpacePath):
        os.makedirs(taskSpacePath)
        #os.chmod(taskSpacePath,stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO)
    with open(userTrackFilePath,"w") as userTrackFile:
        userTrackFile.write(datetime.now().strftime('%d %b %Y %H:%M:%S')+" - "+taskName+" - "+taskSpaceName)
    return taskSpacePath,userSpacePath,userTrackFilePath

