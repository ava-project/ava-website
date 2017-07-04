import json
import os
from zipfile import ZipFile

from avasdk.plugins.hasher import hash_plugin

from django.core.management.base import BaseCommand
from plugins.models import Release


class Command(BaseCommand):
    help = 'Refetch information about plugins'

    def handle(self, *args, **options):
        for release in Release.objects.all():
            self.fix_plugin(release)

    def get_prefix(self, archive):
        files = archive.namelist()
        return os.path.commonpath(files)

    def get_manifest_from_archive(self, plugin):
        plugin.archive.open()
        with ZipFile(plugin.archive) as archive:
            prefix = self.get_prefix(archive)
            with archive.open('{}/manifest.json'.format(prefix)) as myfile:
                manifest = json.loads(myfile.read())
        plugin.archive.close()
        return manifest

    def get_readme_from_archive(self, plugin):
        plugin.archive.open()
        with ZipFile(plugin.archive) as archive:
            prefix = self.get_prefix(archive)
            try:
                with archive.open('{}/README.md'.format(prefix)) as myfile:
                    readme = myfile.read()
            except KeyError:
                readme = None
        plugin.archive.close()
        return readme

    def get_checksum_from_archive(self, plugin):
        path = plugin.archive.path
        return hash_plugin(path)

    def fix_plugin(self, release):
        print('Fix {}'.format(release))
        manifest = self.get_manifest_from_archive(release)
        readme = self.get_readme_from_archive(release)
        release.checksum = self.get_checksum_from_archive(release)
        if readme:
            release.set_readme(readme)
        release.save()
        if 'tags' in manifest:
            release.add_tags(manifest['tags'])
        release.add_commands(manifest.get('commands', []))
