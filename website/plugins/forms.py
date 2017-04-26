import os
from zipfile import ZipFile, BadZipFile

from django import forms
from django.core.validators import ValidationError

from .validators import ZipArchiveValidator


class PluginArchiveField(forms.FileField):
    default_validators = [ZipArchiveValidator()]
    label = 'Plugin .zip'

    def get_prefix(self, archive):
        files = archive.namelist()
        return os.path.commonpath(files)


    def get_manifest(self, archive):
        try:
            with ZipFile(archive.temporary_file_path()) as plugin:
                prefix = self.get_prefix(plugin)
                with plugin.open('{}/manifest.json'.format(prefix)) as myfile:
                    return myfile.read()
        except BadZipFile:
            raise ValidationError('Bad .zip format')
        except FileNotFoundError:
            raise ValidationError('Error with upload, please try again')
        except KeyError:
            raise ValidationError('No manifest.json found in archive')
        except Exception as e:
            print('----------------')
            print(e)
            print('----------------')


    def clean(self, data, initial=None):
        f = super().clean(data, initial)
        manifest = self.get_manifest(f)
        return {
            'zipfile': f,
            'manifest': manifest
        }


class UploadPluginForm(forms.Form):
    archive = PluginArchiveField()
