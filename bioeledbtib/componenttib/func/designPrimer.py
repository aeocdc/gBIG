# -*- coding:utf-8 -*-
def revSeq(dna_seq):
    rev_seq = ''
    complement = {'A':'T','G':'C','C':'G','T':'A'}
    dna_seq = list(dna_seq)
    for i in dna_seq:
        rev_seq += complement[i]
    rev_seq = rev_seq[::-1]
    return rev_seq

#backup
def primer20(seq1,seq2,seq3):
    ##forwardPrimer
    frag1=seq1.upper()[len(seq1)-20:]
    frag2=seq2.upper()[:20]
    forwardPrimer=frag1+frag2
    
    ##reversePrimer
    rev_seq3=revSeq(seq3.upper())
    frag3=rev_seq3[len(seq3)-20:]
    rev_seq2=revSeq(seq2.upper())
    frag4=rev_seq2[:20]
    reversePrimer=frag3+frag4
    
    return forwardPrimer,reversePrimer

def gcPercent(seq):
    #GC percent
    seq=seq.strip()
    from collections import Counter 
    c=Counter(seq)
    #gcPercent 40－60%
    gcPercent=(c['G']+c['C'])/float(len(seq))
    return gcPercent

def tmValue(seq):
    #tm值
    #=ROUND(81.5+(16.6*LOG10(0.1))+(41*((SUMPRODUCT((MID(B2,ROW($1:$98),1)="G")*1)+SUMPRODUCT((MID(B2,ROW($1:$98),1)="C")*1))/LEN(TRIM(B2)))-(600/LEN(TRIM(B2)))),1)
    seq=seq.strip()
    import math
    tmValue=round(81.5+(16.6*math.log10(0.1))+(41*(gcPercent(seq))-(600/float(len(seq)))),1)
    return tmValue    

def primer(seq1,seq2,seq3,len_ha):
    #seq2 target gene
    #len_ha length of homologous arm
    
    #引物靶基因部分长度范围
    min_len_best=20
    max_len_best=25
    min_len=17
    max_len=30
    
    max_diff_tmValue=5
    
    #backup
    #initial Primer
#     forwardPrimer=seq1.upper()[-(len_ha):]+seq2.upper()[:len_ha]
#     reversePrimer=revSeq(seq3.upper())[-(len_ha):]+revSeq(seq2.upper())[:len_ha]

    warningStr=""
    if(len(seq1)<len_ha):
        warningStr+="seq1 length is less than %d. "%(len_ha)
    if(len(seq3)<len_ha):
        warningStr+="seq3 length is less than %d. "%(len_ha)
    if(len(seq2)<min_len):
        warningStr+="seq2 length is less than %d. "%(len_ha)
    ##forward
    seq1_ok=seq1.upper()
    frag1=seq1_ok[-(len_ha):]
    seq2_ok=seq2.upper()
    ##reverse
    seq3_ok=revSeq(seq3.upper())
    frag3=seq3_ok[-(len_ha):]
    seq4_ok=revSeq(seq2.upper())
    
    import re
    pattern = re.compile(r'[^ATGC]')
    if(pattern.search(seq1_ok)):
        warningStr+="seq1 has illegal character. "
    if(pattern.search(seq2_ok)):
        warningStr+="seq2 has illegal character. "
    if(pattern.search(seq3_ok)):
        warningStr+="seq3 has illegal character. "
    
    #1best<->2best
    for i in xrange(min_len_best,(max_len_best+1)):
        frag2=seq2_ok[:i]
        forwardPrimer=frag1+frag2
        for j in xrange(min_len_best,(max_len_best+1)):
            frag4=seq4_ok[:j]
            reversePrimer=frag3+frag4
            
            diff_tmValue=abs(tmValue(forwardPrimer)-tmValue(reversePrimer))
            if (diff_tmValue<max_diff_tmValue):
                return forwardPrimer,reversePrimer,frag1,frag2,frag3,frag4,warningStr
    #1best+longer<->2best+longer
    for i in xrange(min_len_best,(max_len+1)):
        frag2=seq2_ok[:i]
        forwardPrimer=frag1+frag2
        for j in xrange(min_len_best,(max_len+1)):
            frag4=seq4_ok[:j]
            reversePrimer=frag3+frag4
            
            diff_tmValue=abs(tmValue(forwardPrimer)-tmValue(reversePrimer))
            if (diff_tmValue<max_diff_tmValue):
                return forwardPrimer,reversePrimer,frag1,frag2,frag3,frag4,warningStr
    #1shorter+best<->2shorter+best
    for i in xrange(min_len,(max_len_best+1)):
        frag2=seq2_ok[:i]
        forwardPrimer=frag1+frag2
        for j in xrange(min_len,(max_len_best+1)):
            frag4=seq4_ok[:j]
            reversePrimer=frag3+frag4
            
            diff_tmValue=abs(tmValue(forwardPrimer)-tmValue(reversePrimer))
            if (diff_tmValue<max_diff_tmValue):
                return forwardPrimer,reversePrimer,frag1,frag2,frag3,frag4,warningStr
    #1all<->2all
    for i in xrange(min_len,(max_len+1)):
        frag2=seq2_ok[:i]
        forwardPrimer=frag1+frag2
        for j in xrange(min_len,(max_len+1)):
            frag4=seq4_ok[:j]
            reversePrimer=frag3+frag4
            
            diff_tmValue=abs(tmValue(forwardPrimer)-tmValue(reversePrimer))
            if (diff_tmValue<max_diff_tmValue):
                return forwardPrimer,reversePrimer,frag1,frag2,frag3,frag4,warningStr
    #else
    warningStr+="Different of TM value is larger than %d. "%(max_diff_tmValue)
    frag1=seq1_ok[-(len_ha):]
    frag2=seq2_ok[:len_ha]
    frag3=seq3_ok[-(len_ha):]
    frag4=seq4_ok[:len_ha]
    forwardPrimer=frag1+frag2
    reversePrimer=frag3+frag4
    return forwardPrimer,reversePrimer,frag1,frag2,frag3,frag4,warningStr

    
    
def primerList(assembleComponentList,len_ha):
    primerDictList=[]
    length=len(assembleComponentList)
    for i in xrange(length):
        if(0<i<(length-1)):
            middle=assembleComponentList[i]
            if(middle["isTarget"]):
                former=assembleComponentList[i-1]
                latter=assembleComponentList[i+1]
                primerDict={}
                primerDict["formerName"]=former["name"]
                primerDict["middleName"]=middle["name"]
                primerDict["latterName"]=latter["name"]
                primerDict["forward_sequence"],primerDict["reverse_sequence"],primerDict["frag1"],primerDict["frag2"],primerDict["frag3"],primerDict["frag4"],warningStr=primer(former["sequence"],middle["sequence"],latter["sequence"],len_ha)
                primerDict["forward_gcPercent"]=gcPercent(primerDict["forward_sequence"])
                primerDict["reverse_gcPercent"]=gcPercent(primerDict["reverse_sequence"])
                primerDict["forward_tmValue"]=tmValue(primerDict["forward_sequence"])
                primerDict["reverse_tmValue"]=tmValue(primerDict["reverse_sequence"])
                if(warningStr):
                    primerDict["warningStr"]=warningStr
                
                primerDictList.append(primerDict)
    return primerDictList


import unittest

class TestThis(unittest.TestCase):
    def test_all(self):
        seq1="ATAATGTTGACAATTAATCATCCGG"
        seq2="GGCTTTCATTATACGAGCCGGA"
        
        print tmValue(seq1),tmValue(seq2),tmValue(seq1)-tmValue(seq2)
        
        
    def test_tmValue(self):
        seq1="ATTTGCGGCCGCTTGACATTGATTAATCCATGTGCTATAATGGACTACCATGGAATTCAAGGAGATATAG"
        seq2="ATTTGCGGCCGCGGAGATTTGACATTTTGTTTTTGTTCTGTTACATTTGTTTTTTACCATGGAATTCAAGGAGATATAG"
        
        self.assertEqual(tmValue(seq1), 72.7)
        self.assertEqual(tmValue(seq2), 71.8)
        
#     def test_primer_primer20(self):
#         seq1="ATTTGCGGCCGCTTGACATTGATTAATCCATGTGCTATAATGGACTACCATGGAATTCAAGGAGATATAG"
#         seq2="ATTTGCGGCCGCGGAGATTTGACATTTTGTTTTTGTTCTGTTACATTTGTTTTTTACCATGGAATTCAAGGAGATATAG"
#         seq3="GATTTGCGGCCGCTTGACATTGATTAATCCATGTGCTATAATGGACTACCATGGAATTCAAGGAGATATAG"
#         
#         self.assertEqual(primer(seq1,seq2,seq3,20), primer20(seq1,seq2,seq3))