import json, os
from zipfile import ZipFile, BadZipFile

from avasdk.validate_plugin import validate_plugin
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
                    manifest = json.loads(myfile.read())
                errors = validate_plugin(manifest)
                if len(errors):
                    raise ValidationError('Error in manifest.json ({})'.format(errors))
                return manifest
        except BadZipFile:
            raise ValidationError('Bad .zip format')
        except FileNotFoundError:
            raise ValidationError('Error with upload, please try again')
        except KeyError:
            raise ValidationError('No manifest.json found in archive')
        except json.JSONDecodeError:
            raise ValidationError('Error with manifest.json, bad Json Format')

    def clean(self, data, initial=None):
        f = super().clean(data, initial)
        manifest = self.get_manifest(f)
        return {
            'zipfile': f,
            'manifest': manifest
        }


class UploadPluginForm(forms.Form):
    archive = PluginArchiveField()
