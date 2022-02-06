from logging import PlaceHolder
from attr import fields
from django import forms
from .models import Rtdatas, Plandatas, Stracturedatas, Ctdatas, Memo

class CreateRtdataForm(forms.ModelForm):
    region = forms.CharField(label='照射部位')

    class Meta:
        model = Rtdatas
        fields = ('region',)

class DeleteRtdataForm(forms.ModelForm):

    class Meta:
        model = Rtdatas
        fields = []


class PostMemoForm(forms.ModelForm):
    title = forms.CharField(label='タイトル', widget=forms.Textarea(attrs={'rows': 1, 'placeholder':'タイトル'}))
    memo = forms.CharField(label='本文', widget=forms.Textarea(attrs={'placeholder':'本文'}))

    class Meta:
        model = Memo
        fields = ('memo',)