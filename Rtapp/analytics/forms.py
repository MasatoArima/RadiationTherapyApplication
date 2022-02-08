from logging import PlaceHolder
from attr import fields
from django import forms
from .models import Rtdatas, Plandatas, Stracturedatas, Ctdatas, Memo
from datetime import datetime

class CreateRtdataForm(forms.ModelForm):
    region = forms.CharField(label='照射部位')

    class Meta:
        model = Rtdatas
        fields = ['region',]

    def save(self, *args, **kwargs):
        obj = super(CreateRtdataForm, self).save(commit=False)
        obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        obj.save()
        return obj

class UpdateRtdataForm(forms.ModelForm):

    class Meta:
        model = Rtdatas
        fields = ['region',]

    def save(self, *args, **kwargs):
        obj = super(UpdateRtdataForm, self).save(commit=False)
        obj.update_at = datetime.now()
        obj.save()
        return obj



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


class PlandataUploadForm(forms.ModelForm):
    plandata = forms.FileField(required=False)

    class Meta:
        model = Plandatas
        fields = ['plandata',]

    def save(self, *args, **kwargs):
        obj = super(PlandataUploadForm, self).save(commit=False)
        obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        obj.rtdata = kwargs['rtdata']
        obj.save()
        return obj

class StracturedataUploadForm(forms.ModelForm):
    stracturedata = forms.FileField(required=False)

    class Meta:
        model = Stracturedatas
        fields = ['stracturedata',]

    def save(self, *args, **kwargs):
        obj = super(StracturedataUploadForm, self).save(commit=False)
        obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        obj.rtdata = kwargs['rtdata']
        obj.save()
        return obj

class CtdataUploadForm(forms.ModelForm):
    ctdata = forms.FileField(required=False)

    class Meta:
        model = Ctdatas
        fields = ['ctdata',]

    def save(self, *args, **kwargs):
        obj = super(CtdataUploadForm, self).save(commit=False)
        obj.create_at = datetime.now()
        obj.update_at = datetime.now()
        obj.rtdata = kwargs['rtdata']
        obj.save()
        return obj