#coding=utf-8
'''
Created on 20170222

@author: Huang Teng
@summary: 封装db操作
'''
import logging
#logger = logging.getLogger("developing")#debug log
logger = logging.getLogger(__name__)
'''import logOperator
logging=logOperator.getLogging('./logs/dbOperator.log')'''

def sqlSelect(sqlString,dbCursor):
    try:
        logger.debug(sqlString)
        logger.debug(dbCursor.execute(sqlString))
        sqlResultCount=dbCursor.rowcount
        sqlResultData = dbCursor.fetchall()
        if(sqlResultCount):
            logger.debug(sqlResultData[0][1])
        #sqlResultData=[[str(inner_2) for inner_2 in inner_1] for inner_1 in sqlResultData]#中文时报错'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
        return sqlResultData,sqlResultCount
    except:
        logger.exception(sqlString)
       
def sqlDo(sqlString,dbCursor,dbConn):
    try:
       dbCursor.execute(sqlString)
       # 提交修改
       dbConn.commit()
    except:
       # 发生错误时回滚
       logger.exception(sqlString)
       dbConn.rollback()
       
