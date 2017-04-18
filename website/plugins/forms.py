from django import forms


class UploadPluginForm(forms.Form):
    archive = forms.FileField(label='Plugin .zip')
