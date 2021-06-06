from django.conf import settings

if settings.APP_NAME == 'flourish_metadata_rules':
    from .tests import models
