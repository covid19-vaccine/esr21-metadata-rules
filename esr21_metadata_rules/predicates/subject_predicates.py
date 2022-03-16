from django.apps import apps as django_apps
from edc_constants.constants import FEMALE, YES, NEG
from edc_metadata_rules import PredicateCollection


class SubjectPredicates(PredicateCollection):

    app_label = 'esr21_subject'
    visit_model = f'{app_label}.subjectvisit'

    def func_participant_female(self, visit=None, **kwargs):
        """Returns true the participant is female."""

        informed_consent_cls = django_apps.get_model('esr21_subject.informedconsent')

        try:
            informed_consent_obj = informed_consent_cls.objects.filter(
                subject_identifier=visit.appointment.subject_identifier).latest('')
        except informed_consent_cls.DoesNotExist:
            return False
        else:
            return informed_consent_obj.gender == FEMALE

    def func_serious_ae_required(self, visit=None, **kwargs):

        ae_model = django_apps.get_model(f'{self.app_label}.adverseevent')
        try:
            ae_obj = ae_model.objects.get(subject_visit=visit)
        except ae_model.DoesNotExist:
            return False
        else:
            return ae_obj.adverseeventrecord_set.filter(serious_event=YES).count() != 0

    def func_special_interest_ae_required(self, visit=None, **kwargs):

        ae_model = django_apps.get_model(f'{self.app_label}.adverseevent')
        try:
            ae_obj = ae_model.objects.get(subject_visit=visit)
        except ae_model.DoesNotExist:
            return False
        else:
            return ae_obj.adverseeventrecord_set.filter(special_interest_ae=YES).count() != 0

    def func_symptomatic_infection_enrol(self, visit=None, **kwargs):

        screening_model = django_apps.get_model(f'{self.app_label}.screeningeligibility')
        covid19_results_obj = self.covid19_results_obj(visit)

        try:
            screening_obj = screening_model.objects.get(
                subject_identifier=visit.subject_identifier)
        except screening_model.DoesNotExist:
            return False
        else:
            cond = True if not covid19_results_obj or\
             covid19_results_obj.covid_result != NEG else False
            if visit.visit_code == '1000' and cond:
                return screening_obj.symptomatic_infections_experiences != YES
            else:
                return True

    def covid19_results_obj(self, visit):
        covid19_results_model = django_apps.get_model(f'{self.app_label}.covid19results')
        try:
            covid19results_obj = covid19_results_model.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code=visit.visit_code
                )
        except covid19_results_model.DoesNotExist:
            return None
        else:
            return covid19results_obj
