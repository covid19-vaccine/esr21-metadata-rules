from django.apps import AppConfig as DjangoAppConfig
from django.core.management.color import color_style

style = color_style()


class AppConfig(DjangoAppConfig):
    name = 'esr21_metadata_rules'
    verbose_name = 'ESR21 METADATA RULES'
