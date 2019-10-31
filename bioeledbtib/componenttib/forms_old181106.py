#coding=utf-8
'''
Created on 20170502
@author: Huang Teng
@summary: forms for componenttib
'''
from django import forms

class Component5DesignForm(forms.Form):
#     len_ha=forms.IntegerField(label="Length of homologous arm",min_value=0)
#     organism=forms.ChoiceField(label="organism", choices=(("E.coli","E.coli"),("S.cerevisiae","S.cerevisiae"),("C.glutamicum","C.glutamicum"),),initial="E.coli",required=True,)
    pass
class DesignModuleForm(forms.Form):
    pass
class SendAssembleForm(forms.Form):
    pass
class SearchComponentForm(forms.Form):
    symbolType=forms.ChoiceField(label="symbol type", choices=(("enzymeId","enzyme Id"),("substrateName","substrate Name"),("productName","product Name"),),initial="enzymeId",required=True,)
    symbolValue=forms.CharField(label="symbol for query", max_length=50,required=True,help_text="example: enzyme Id: KRED027 | substrate Name: COBE | product Name: ATS-4",)
class Sgrna5DesignForm(forms.Form):
    geneFile8Upload=forms.FileField(label="target gene file", required=True,)
    #backup modelFile8Upload=forms.FileField(label="model File by upload", required=True, widget=forms.FileInput(attrs={"onchange":"verifyExtension(this,'.txt')"}),)
    #backup dtgeneSequence=forms.CharField(label="Deletion target gene sequence",widget=forms.Textarea(),required=True,help_text="gene sequence",)
    referenceFile8Upload=forms.FileField(label="reference genome file", required=True,)
    userEmail=forms.EmailField(label="Email address",required=True,help_text="email address",)

formDict={'component5Design': Component5DesignForm,
          'designModule': DesignModuleForm,
          'sendAssemble':SendAssembleForm,
          'searchComponent': SearchComponentForm,
          'sgrna5Design':Sgrna5DesignForm,
          }
