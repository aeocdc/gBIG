# -*- coding:utf-8 -*-
'''
Created on 20170222

@author: Huang Teng
@summary: 封装db操作
'''
import logging
#logger = logging.getLogger("developing")#debug log
logger = logging.getLogger(__name__)

def sqlSelect(sqlString,dbCursor):
    try:
        logger.debug(sqlString)
        dbCursor.execute(sqlString)
        sqlResultCount=dbCursor.rowcount
        sqlResultData = dbCursor.fetchall()
        
        #sqlResultData=[[str(inner_2) for inner_2 in inner_1] for inner_1 in sqlResultData]#中文时报错'ascii' codec can't encode characters in position 0-1: ordinal not in range(128)
        return sqlResultData,sqlResultCount
    except:
        logger.exception(sqlString)
def sqlDo(sqlString,dbCursor,dbConn):
    try:
        logger.debug(sqlString)
        dbCursor.execute(sqlString)
        # 提交修改
        dbConn.commit()
        return True
    except:
        # 发生错误时回滚
        logger.exception(sqlString)
        dbConn.rollback()
        return False
       

def prepareDb():
    import MySQLdb
    from componenttib.properties import dbProperties
    dbConn = MySQLdb.connect(host=dbProperties["dbHost"],user=dbProperties["dbUser"],passwd=dbProperties["dbPw"],db=dbProperties["dbName"],charset='utf8')
    dbCursor = dbConn.cursor()
    return dbConn,dbCursor

