from django.core.management.base import BaseCommand, CommandError
from plugins.models import Release


class Command(BaseCommand):
    help = 'Refetch information about plugins'

    def handle(self, *args, **options):
        for release in Release.objects.all():
            self.fix_plugin(release)


    def fix_plugin(self, release):
        print('Fix {}'.format(release))
        manifest = release.get_manifest_from_archive()
        readme = release.get_readme_from_archive()
        if readme:
            release.set_readme(readme)
        release.save()
        if 'tags' in manifest:
            release.add_tags(manifest['tags'])
        release.add_commands(manifest.get('commands', []))
