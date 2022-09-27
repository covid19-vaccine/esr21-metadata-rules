from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register

from ..predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class CrfPregnancyTestRuleGroup(CrfRuleGroup):

    vaccination_details = CrfRule(
        predicate=pc.func_pos_pregnancy_vax_nrequired,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.vaccinationdetails', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.pregnancytest'
