from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P
from edc_constants.constants import YES

from ..predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class pregnancyStatusRuleGroup(CrfRuleGroup):

    pregnancy_test = CrfRule(
        predicate=pc.func_preg_test_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pregnancytest', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.pregnancystatus'
