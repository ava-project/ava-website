import zipfile

from django import forms

from .validators import ZipArchiveValidator


class PluginArchiveField(forms.FileField):
    default_validators=[ZipArchiveValidator()]
    label='Plugin .zip'


    def to_python(self, data):
        return super().to_python(data)


class UploadPluginForm(forms.Form):
    archive = PluginArchiveField()
