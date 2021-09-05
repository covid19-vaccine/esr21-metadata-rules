from django.apps import apps as django_apps
from edc_constants.constants import FEMALE
from edc_metadata_rules import PredicateCollection


class SubjectPredicates(PredicateCollection):

    app_label = 'esr21_subject'
    visit_model = f'{app_label}.subjectvisit'

    def func_participant_female(self, visit=None, **kwargs):
        """Returns true the participant is female."""

        informed_consent_cls = django_apps.get_model('esr21_subject.informedconsent')

        try:
            informed_consent_obj = informed_consent_cls.objects.get(
                subject_identifier=visit.appointment.subject_identifier)
        except informed_consent_cls.DoesNotExist:
            return False
        else:
            return informed_consent_obj.gender == FEMALE

    def func_women_child_bearing_age(self, visit=None, **kwargs):

        pass
