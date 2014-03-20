"""Just some test settings"""
from django.conf import global_settings

# Detect location and available modules
import os
test_root = os.path.dirname(os.path.realpath(__file__))

DEBUG = False  # will be False anyway by DjangoTestRunner.
TEMPLATE_DEBUG = False
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:'
    }
}
TEMPLATE_DIRS = (os.path.join(test_root, 'templates'), ),
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)
TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS + (
    'django.core.context_processors.request',
)
INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',

    'rest_framework',
    'polymorphic',
    'elastimorphic',

    'bulbs.content',
    'bulbs.images',

    'tests.testcontent'  # Just here for a couple of test models
)
SITE_ID = 3
SECRET_KEY = '_(m&)4jinh6cuzjt&p37lbg8ycc3d*xd36!pl3g*n2m3is_89v'

ROOT_URLCONF = 'tests.urls',

BETTY_CROPPER = {
        'ADMIN_URL': 'http://localhost:8698/',
        'PUBLIC_URL': 'http://localhost:8698/',
        'DEFAULT_IMAGE': '12345'
}