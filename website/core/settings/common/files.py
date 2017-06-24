# de

#
FILE_UPLOAD_HANDLERS = [
    'django.core.files.uploadhandler.TemporaryFileUploadHandler'
]

STATIC_URL = '/static/'
STATIC_ROOT = '/app/public'
MEDIA_ROOT = '/data'

STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'PIPELINE_ENABLED': True,
    'STYLESHEETS': {
        'stats': {
            'source_filenames': (
              'js/jquery.js',
              'js/d3.js',
              'js/collections/*.js',
              'js/application.js',
            ),
            'output_filename': 'js/stats.js',
        }
    }
}
