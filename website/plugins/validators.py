import zipfile

from django.core.validators import FileExtensionValidator
from django.core.validators import ValidationError


class ZipArchiveValidator(FileExtensionValidator):
    message_bad_ext = 'Only zip archived are allowed'
    message_wrong_archive = 'Bad .zip format'

    def __init__(self):
        return super().__init__(['zip'], self.message_bad_ext)

    def __call__(self, value):
        super().__call__(value)
        if not zipfile.is_zipfile(value.temporary_file_path()):
            raise ValidationError(self.message_wrong_archive)
