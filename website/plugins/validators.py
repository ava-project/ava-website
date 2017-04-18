from django.core.validators import FileExtensionValidator

class ZipArchiveValidator(FileExtensionValidator):

    def __init__(self):
        return super().__init__(['zip'],
            'Only zip archived are allowed')
