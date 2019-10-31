# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
'''
Created on Jul 2, 2018
Modified on Jul , 2018
@author: Teng Huang
@summary: fasta文件处理
'''
import os

import logging
#backup 无效 logging.basicConfig(level=logging.DEBUG)#temp log
logger = logging.getLogger("developing")#debug log

def one_line(inputFilePath,outputFilePath):
	#序列变一行
	content=""
	with open(outputFilePath,"w") as oFile:
		with open(inputFilePath) as iFile:
			for line in iFile:
				if line.startswith(">"):
					oFile.write("\n"+line.strip().replace(" ","_")+"\n")
				else:
					oFile.write(line.strip())
		oFile.write("\n")
					
				
		'''backup 问题未知
		contentList=content.split(">")[1:]#分割为基因
		#合并
		for gene in contentList:
			sequence_oneLine=""
			name=gene.split("\n")[0].strip()
			name=">"+name
			oFile.write(name+"\n")
			
			sequences=gene.split("\n")[1:]
			for sequence in sequences:
				oFile.write(sequence.strip())
				
			oFile.write("\n")'''
	
	
	
	