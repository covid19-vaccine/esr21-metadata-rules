from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from edc_metadata import NOT_REQUIRED, REQUIRED

from ..predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class SubjectVisitRuleGroup(CrfRuleGroup):

    pregnancy = CrfRule(
        predicate=pc.func_participant_female,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pregnancystatus', ])

    covid_symptoms = CrfRule(
        predicate=pc.func_symptomatic_infection_enrol,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.physicalexam',
                       f'{app_label}.vaccinationdetails'])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.subjectvisit'
