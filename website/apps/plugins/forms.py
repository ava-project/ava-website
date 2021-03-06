import json
import os
import avasdk

from zipfile import ZipFile, BadZipFile

from avasdk.plugins.manifest import validate_manifest
from avasdk.plugins.hasher import hash_plugin
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
                prefix = prefix + '/' if len(prefix) else ''
                with plugin.open('{}manifest.json'.format(prefix)) as myfile:
                    manifest = json.loads(myfile.read())
                validate_manifest(manifest)
                return manifest
        except BadZipFile:
            raise ValidationError('Bad .zip format')
        except FileNotFoundError:
            raise ValidationError('Error with upload, please try again')
        except KeyError:
            raise ValidationError('No manifest.json found in archive')
        except json.JSONDecodeError:
            raise ValidationError('Error with manifest.json, bad Json Format')
        except avasdk.exceptions.ValidationError as e:
            raise ValidationError('Error in manifest.json ({})'.format(e))

    def get_readme(self, archive):
        try:
            with ZipFile(archive.temporary_file_path()) as plugin:
                prefix = self.get_prefix(plugin)
                prefix = prefix + '/' if len(prefix) else ''
                with plugin.open('{}/README.md'.format(prefix)) as myfile:
                    readme = myfile.read()
                return readme
        except FileNotFoundError:
            raise ValidationError('Error with upload, please try again')
        except KeyError:
            return None

    def clean(self, data, initial=None):
        f = super().clean(data, initial)
        manifest = self.get_manifest(f)
        readme = self.get_readme(f)
        return {
            'zipfile': f,
            'manifest': manifest,
            'readme': readme,
            'checksum': hash_plugin(f.temporary_file_path()),
        }


class UploadPluginForm(forms.Form):
    archive = PluginArchiveField()
