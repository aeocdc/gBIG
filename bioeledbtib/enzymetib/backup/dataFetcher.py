#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: Fetch data，未启用
'''

def selectALLData(tableName,parameterDic):
    import MySQLdb
    import dbOperator as dbor
    from properties import folderDic,dbProperties
    dbConn = MySQLdb.connect(dbProperties["dbHost"],dbProperties["dbUser"],dbProperties["dbPw"],dbProperties["dbName"] )
    dbCursor = dbConn.cursor()
    #fetch data
    parameterData=[]
    parameterTitle=[]
    for k,v in parameterDic.iteritems():
        parameterData.append(v)
        parameterTitle.append(k)
    sqlString="select * from "+tableName+" where ("+(",".join(parameterTitle))+")=('"+("','".join(parameterData))+"')"
    logging.debug(sqlString)
    return dbor.sqlSelect(sqlString,dbCursor)

