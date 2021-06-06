from django.db import models
from edc_base.model_mixins import BaseUuidModel


class InformedConsent(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    gender = models.CharField(max_length=25)
