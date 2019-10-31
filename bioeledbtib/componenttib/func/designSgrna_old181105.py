# -*- coding:utf-8 -*-
from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
'''
Created on Mar 21, 2018
Modified on Jun 5, 2018
@author: Teng Huang
@summary: 设计sgRNA。sgRNAcas9+自定义处理提取
'''
import os

import logging
#backup 无效 logging.basicConfig(level=logging.DEBUG)#temp log
logger = logging.getLogger("developing")#debug log

#执行cmd
def cmd(cmdString):
    logger.debug(cmdString.split(" "))
    import subprocess
    try:
        what=subprocess.check_output(cmdString.split(" "))
        logger.debug(what)
    except subprocess.CalledProcessError as e:
        logger.error(e.output)
        
#sgrna
def sgrnacas9(taskSpacePath,geneFilePath,referenceFilePath):
    #backup 
    #import uuid
    #taskSpacePath="/media/huangteng/data_cas9/"+str(uuid.uuid5(uuid.uuid1(), 'sgrnaFolder'))+"/"
    
    #处理参考基因组文件，变一行
    [fname,fename]=os.path.splitext(referenceFilePath)
    [dirname,filename]=os.path.split(fname)
    referenceOneLineFilePath=os.path.join(dirname,filename.replace(" ","_")+"_one_line"+fename)
    from .fasta_dispose import *
    one_line(referenceFilePath,referenceOneLineFilePath)
    
    #处理基因文件，加长度
    gene5lenghFilePath=os.path.join(taskSpacePath,"gene5lengh.txt")#基因文件，带基因长度
    from .addSeqLength import *
    addSeqLength(geneFilePath,gene5lenghFilePath)
    
    #sgTNAcas9
    sgrnaAppFilePath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/sgRNAcas9_3.0.5.ht.pl"
    seqmapAppFolderPath="/home/webservice/outlab/cas9/sgRNAcas9_3.0.5/Seqmap"
    
    cmdString_sgrna="perl "+sgrnaAppFilePath+" -i "+gene5lenghFilePath+" -g "+referenceOneLineFilePath+" -n 0 -o b -t s -v l -p "+taskSpacePath+" -pseqmap "+seqmapAppFolderPath
    cmd(cmdString_sgrna)
        
    sgrnaFolder=os.path.join(taskSpacePath,"sgRNAcas9_report")#结果目录
    
    #所需结果文件并改为txt
    sg_report_FilePath=os.path.join(sgrnaFolder,"sgRNAcas9_report.txt")
    os.rename(os.path.join(sgrnaFolder,"sgRNAcas9_report.xls"),sg_report_FilePath)
    
    #自定义处理提取
    nxmAppFilePath="/home/webservice/bioeledbtib/componenttib/func/check_sgRNA_C_all-end.pl"
    sgRNA_rm_repeatFilePath=os.path.join(sgrnaFolder,"sgRNA_rm_repeat.txt")#处理结果文件
    cmdString_sgrna2="perl "+nxmAppFilePath+" -i "+sg_report_FilePath+" -o "+sgRNA_rm_repeatFilePath
    cmd(cmdString_sgrna2)
    
    #提取存在可编辑位点的结果
    title=["sgRID","Start","End","Protospacer_sequence+PAM(5'-3')","Length(nt)","GC%_of_Protospacer","Protospacer+PAM(OT)","0M(on-/off-)","1M","2M","3M","4M","5M","Total_No.of_OT","Seed_12+PAM(POT)","0M(on-/off-)","1M","2M","3M","4M","5M","Total_No.of_POT","Risk_evaluation","1st target codon","Editable for forming an early stop codonb","Position of C relative to PAM","Position of C inside the gene (%)","2st target codon","Editable for forming an early stop codonb","Position of C relative to PAM","Position of C inside the gene (%)"]
    '''sgRNA_result_editableFilePath=os.path.join(sgrnaFolder,"sgRNA_result_editable.txt")#处理结果文件
    with open(sgRNA_result_editableFilePath, 'w') as oFile:
        oFile.write('\t'.join(title)+'\n')
        with open(sgRNA_rm_repeatFilePath, 'rU') as iFile:
            for line in iFile:
                line = line.strip().split('\t')
                if len(line) ==27:
                    if int(line[24]) == 1:
                        oFile.write('\t'.join(line)+'\n')
                elif len(line) ==31:
                    if int(line[24]) == 1 or int(line[28]) == 1:
                        oFile.write('\t'.join(line)+'\n')'''
    import csv
    sgRNA_result_editableFilePath=os.path.join(sgrnaFolder,"sgRNA_result_editable.csv")#处理结果文件
    with open(sgRNA_result_editableFilePath, 'wb') as oFile:
        spamwriter = csv.writer(oFile, delimiter=str(','))
        spamwriter.writerow(title)
        with open(sgRNA_rm_repeatFilePath, 'rU') as iFile:
            for line in iFile:
                line = line.strip().split('\t')
                if len(line) ==27:
                    if int(line[24]) == 1:
                        spamwriter.writerow(line)
                elif len(line) ==31:
                    if int(line[24]) == 1 or int(line[28]) == 1:
                        spamwriter.writerow(line)
    #backup compress
    '''
    reportFileList=["report_protospacer_pairs.xls","sgRNAcas9_report.xls","CRISPR.targets_single.fa","report_protospacer_single.txt","TargetSeq.fa",]
    sgrna_reportFilePath=taskSpacePath+"sgrna_report.tar"
    import tarfile
    tar=tarfile.open(sgrna_reportFilePath,'w')
    for file in reportFileList:
        fullpath=os.path.join(sgrnaFolder,file)  
        tar.add(fullpath,arcname=file)  
    tar.close()
    return sgrna_reportFilePath
    '''
    sgrna_reportFilePath=sgRNA_result_editableFilePath
    return sgrna_reportFilePath