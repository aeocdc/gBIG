#coding=utf-8
'''
Created on 20170222

@author: Huang Teng
@summary: 封装logging操作
'''
def printProgress(currentCount,totalCount):
    modulus=currentCount%10
    percent=100.0*currentCount/totalCount
    threshold=10
    if ((modulus==0) or (percent>threshold)):
        threshold+=threshold
        return True,percent
    else:
        return False,percent
    
def getLogging(logFilePath):
    import os
    logFileFolder=os.path.dirname(logFilePath)
    if (not os.path.exists(logFileFolder)):
        os.makedirs(logFileFolder)
    import logging
    logging.basicConfig(level=logging.DEBUG,
                    format='%(levelname)s-%(asctime)s-%(filename)s[line:%(lineno)d]: %(message)s',
                    datefmt='%d %b %Y %H:%M:%S',
                    filename=logFilePath,
                    filemode='w')
    #定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象#
    console = logging.StreamHandler()
    console.setLevel(logging.WARN)
    formatter = logging.Formatter('%(levelname)s-%(asctime)s-%(filename)s[line:%(lineno)d]: %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    
    return logging
'''#backup
import logging
try:
    1/0
except Exception:
    logging.exception("Deliberate divide by zero traceback")
'''