#coding=utf-8
'''
Created on 20170302
@author: Huang Teng
@summary: forms for enzymetib
'''
from django import forms

class SearchForm(forms.Form):
    symbolType=forms.ChoiceField(label="symbol type", choices=(("enzymeId","enzyme Id"),("substrateName","substrate Name"),("productName","product Name"),),initial="enzymeId",required=True,)
    symbolValue=forms.CharField(label="symbol for query", max_length=50,required=True,help_text="example: enzyme Id: KRED027 | substrate Name: COBE | product Name: ATS-4",)


formDict={'search': SearchForm,
          }
