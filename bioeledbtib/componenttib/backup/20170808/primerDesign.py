# -*- coding: utf-8 -*-
def revSeq(dna_seq):
    rev_seq = ''
    complement = {'A':'T','G':'C','C':'G','T':'A'}
    dna_seq = list(dna_seq)
    for i in dna_seq:
        rev_seq += complement[i]
    rev_seq = rev_seq[::-1]
    return rev_seq

def designPrimer(seq1,seq2,seq3):
    ##forwardPrimer
    frag1=seq1.upper()[len(seq1)-20:]
    frag2=seq2.upper()[:20]
    forwardPrimer=frag1+frag2
    
    ##reversePrimer
    rev_seq3=revSeq(seq3.upper())
    frag3=rev_seq3[len(seq1)-20:]
    rev_seq2=revSeq(seq2.upper())
    frag4=rev_seq2[:20]
    reversePrimer=frag3+frag4
    
    return forwardPrimer,reversePrimer
if __name__=="__main__":
    seq1='aGCTTTTCATTCTGACTGCAACGGGCAATATGTCTCTGTGTGGA' 
    seq2='aATTACCGGTCAAGGGCATTTCCAATCTGAATAATATGGCAATGTTCAGCGTTTCCGGCCCGGGGATGAA'
    seq3='cGAAGTGTTTGTGATTGGCGTCGGTGGCGTTGGCGGTGCGCTGC'
    forwardPrimer,reversePrimer=designPrimer(seq1,seq2,seq3)
    print forwardPrimer
    print reversePrimer
    
    from collections import Counter 
    c1=Counter(forwardPrimer)
    c2=Counter(reversePrimer)
    #gcPecent 40－60%
    gcPecent4forward=(c1['G']+c1['C'])/float(len(forwardPrimer))
    gcPecent4reverse=(c2['G']+c2['C'])/float(len(reversePrimer))
    print 'gcPecent=',gcPecent