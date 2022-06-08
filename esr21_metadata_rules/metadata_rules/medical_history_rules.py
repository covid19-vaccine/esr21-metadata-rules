from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ..predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class MedicalHistoryRuleGroup(CrfRuleGroup):
    adverse_event = CrfRule(
        predicate=pc.fun_conc_med_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.concomitantmedication', ])


    class Meta:
        app_label = app_label
        source_model = f'{app_label}.medicalhistory'
