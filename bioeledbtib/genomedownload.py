# -*- coding: utf-8 -*-
"""
Created on Mon Dec  3 14:19:17 2018

@author: yy
"""

from obs import ObsClient

obsClient = ObsClient(
    access_key_id='ENLJSZAHPDGFVCYH5JGS',
    secret_access_key='NMfvQFKWVJvyG1ajPj8oU3Az4VPQkJGonqEw8u1O',
    server='https://obs.cn-north-1.myhuaweicloud.com'
    )

resp = obsClient.getObject('hs-grch38.p12-genome', 'genome/GRCh38.p12_part1.fna', downloadPath='/home/webservice/ref/GRCh38.p12_part1.fna')
if resp.status < 300:
    # 输出请求Id
    print('requestId:', resp.requestId)
else:
    # 输出错误码
    print('errorCode:', resp.errorCode)

obsClient.close()
