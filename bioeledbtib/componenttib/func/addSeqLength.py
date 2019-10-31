# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
'''
Created on Jun 5, 2018
Modified on Jun 5, 2018
@author: Teng Huang
@summary: 处理基因文件，加长度
'''

def addSeqLength(inputFilePath,outputFilePath):
	content=""
	with open(outputFilePath,"w") as oFile:
		with open(inputFilePath,"r") as iFile:
			for line in iFile.readlines():
				content+=line
		contentList=content.split(">")[1:]#分割为基因
		#计数
		#backup 正则方式，也对
		#import re
		#pattern=re.compile(r'[ATGCatgc]')
		for gene in contentList:
			lengthCount=0
			name=gene.split("\n")[0].strip()
			sequences=gene.split("\n")[1:]
			for sequence in sequences:
				#print(len(pattern.findall(sequence)))#backup 正则方式，也对
				lengthCount+=len(sequence.strip())
			name=">"+str(lengthCount)+"_"+name
			
			oFile.write(name+"\n")
			oFile.writelines(sequences)
			oFile.write("\n")