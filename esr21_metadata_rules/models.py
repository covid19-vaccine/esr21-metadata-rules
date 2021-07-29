from django.conf import settings

if settings.APP_NAME == 'esr21_metadata_rules':
    from .tests import models
