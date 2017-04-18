from django import forms

from .validators import ZipArchiveValidator


class UploadPluginForm(forms.Form):
    archive = forms.FileField(
        label='Plugin .zip',
        validators=[ZipArchiveValidator()]
    )

    # def clean(self):
