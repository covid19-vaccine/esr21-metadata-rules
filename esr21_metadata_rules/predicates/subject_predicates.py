from edc_metadata_rules import PredicateCollection

from django.apps import apps as django_apps
from edc_constants.constants import FEMALE, YES, NEG, POS


class SubjectPredicates(PredicateCollection):
    app_label = 'esr21_subject'
    visit_model = f'{app_label}.subjectvisit'

    @property
    def preg_status(self):
        return django_apps.get_model(f'{self.app_label}.pregnancystatus')

    @property
    def preg_test_cls(self):
        return django_apps.get_model(f'{self.app_label}.pregnancytest')

    @property
    def edc_appointment_cls(self):
        return django_apps.get_model('edc_appointment.appointment')

    @property
    def preg_outcome_cls(self):
        return django_apps.get_model(f'{self.app_label}.pregoutcome')

    def func_participant_female(self, visit=None, **kwargs):
        """Returns true the participant is female."""

        informed_consent_cls = django_apps.get_model('esr21_subject.informedconsent')

        try:
            informed_consent_obj = informed_consent_cls.objects.filter(
                subject_identifier=visit.appointment.subject_identifier).latest('created')
        except informed_consent_cls.DoesNotExist:
            return False
        else:
            if visit.visit_code_sequence > 0:
                return False
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
            return ae_obj.adverseeventrecord_set.filter(
                special_interest_ae=YES).count() != 0

    def func_symptomatic_infection_enrol(self, visit, **kwargs):
        check = self.check_covid_symptomatic(visit)
        return check if check is not None else False

    def func_symptomatic_infection_pcr_enrol(self, visit, **kwargs):
        check = self.check_covid_symptomatic(visit)
        return check if check is not None else True

    def check_covid_symptomatic(self, visit=None):
        # If symptomatic, and no/pos covid results; don't show physical and vaccination form. show SARS-CoV
        # If symptomatic, and neg covid results; show physical and vaccination
        # If not symptomatic show physical and vaccination form. no SARS-CoV
        screening_model = django_apps.get_model(f'{self.app_label}.screeningeligibility')

        try:
            screening_obj = screening_model.objects.get(
                subject_identifier=visit.subject_identifier)
        except screening_model.DoesNotExist:
            return None
        else:
            symptomatic = True if screening_obj.symptomatic_infections_experiences == YES else False
            covid19_results = self.covid19_results_obj(visit)
            enrol_visit = True if visit.visit_code == '1000' and visit.visit_code_sequence == 0 else False
            if enrol_visit and symptomatic:
                if covid19_results and getattr(covid19_results, 'covid_result',
                                               None) == NEG:
                    return True
                return False
            elif enrol_visit and not symptomatic:
                return True
            elif visit.visit_code in ['1070', '1170'] and visit.visit_code_sequence == 0:
                return True
            return None

    def func_preg_test_required(self, visit=None, **kwargs):
        try:
            preg_status_obj = self.preg_status.objects.get(subject_visit=visit)
        except self.preg_status.DoesNotExist:
            return False
        else:
            if visit.visit_code in ['1000', '1070',
                                    '1170'] and visit.visit_code_sequence == 0:
                return preg_status_obj.child_bearing_potential == YES
            return False

    def covid19_results_obj(self, visit):
        covid19_results_model = django_apps.get_model(f'{self.app_label}.covid19results')
        try:
            covid19results_obj = covid19_results_model.objects.get(
                subject_visit__subject_identifier=visit.subject_identifier,
                subject_visit__visit_code=visit.visit_code,
                subject_visit__visit_code_sequence=visit.visit_code_sequence
            )
        except covid19_results_model.DoesNotExist:
            return None
        else:
            return covid19results_obj

    def func_preg_outcome_required(self, visit=None, **kwargs):
        try:
            current_preg = self.preg_test_cls.objects.get(
                subject_visit=visit,
                preg_performed=YES,
                result=NEG)
        except self.preg_test_cls.DoesNotExist:
            return False
        else:
            pregnancies = self.preg_test_cls.objects.filter(
                subject_visit__subject_identifier=visit.subject_identifier,
                preg_performed=YES, result=POS)
            if pregnancies:
                latest_pregnancy = pregnancies.latest('preg_date')

                preg_outcome = self.preg_outcome_cls.objects.filter(
                    subject_visit__subject_identifier=visit.subject_identifier,
                    report_datetime__date__range=(current_preg.preg_date.date(),
                                                  latest_pregnancy.preg_date.date()))

                in_between_neg = self.preg_test_cls.objects.filter(
                    subject_visit__subject_identifier=visit.subject_identifier,
                    result=NEG, preg_date__date__range=(current_preg.preg_date.date(),
                                                        latest_pregnancy.preg_date.date()))
                return (not preg_outcome and current_preg.preg_date.date() >
                        latest_pregnancy.preg_date.date() and not in_between_neg)

            return False

    def fun_enrol_forms_required(self, visit=None, **kwargs):
        inperson_visits = ['1000', '1070', '1170']
        vac_history_cls = django_apps.get_model(
            'esr21_subject.vaccinationhistory')
        try:
            vac_history_obj = vac_history_cls.objects.get(
                subject_identifier=visit.subject_identifier,
                report_datetime__lte=visit.report_datetime)
        except vac_history_cls.DoesNotExist:
            current_appointment = visit.appointment
            if current_appointment.previous_by_timepoint:
                return False
            return visit.visit_code in inperson_visits
        else:
            vaccinated_onstudy = (vac_history_obj.dose1_product_name == 'azd_1222' or
                                  vac_history_obj.dose2_product_name == 'azd_1222')
            return visit.visit_code in inperson_visits and not vaccinated_onstudy

    def fun_conc_med_required(self, visit=None, **kwargs):
        med_history_cls = django_apps.get_model(f'{self.app_label}.medicalhistory')
        med_diagnosis_cls = django_apps.get_model(f'{self.app_label}.medicaldiagnosis')

        try:
            med_history_obj = med_history_cls.objects.get(subject_visit=visit)
        except med_history_cls.DoesNotExist:
            return False
        else:
            conc_med_count = med_diagnosis_cls.objects.filter(
                medical_history=med_history_obj,
                condition_related_meds=YES
            ).count()
            return conc_med_count > 0
