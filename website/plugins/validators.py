from django.core.validators import FileExtensionValidator


class ZipArchiveValidator(FileExtensionValidator):
    message = 'Only zip archived are allowed'

    def __init__(self):
        return super().__init__(['zip'], self.message)

    def __call__(self, value):
        super().__call__(value)
        if not zipfile.is_zipfile(path):
            print('no zipfile')
            raise ValidationError(self.message, code='invalid')
