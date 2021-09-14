from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P
from ..predicates import SubjectPredicates
from edc_constants.constants import YES

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class VaccinationDetailsRuleGroup(CrfRuleGroup):

    adverse_event = CrfRule(
        predicate=P('adverse_event', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.adverseevent', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.vaccinationdetails'
