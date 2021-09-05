from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P
from edc_constants.constants import YES

app_label = 'esr21_subject'


@register()
class pregnancyStatusRuleGroup(CrfRuleGroup):

    pregnancy_test = CrfRule(
        predicate=P('child_bearing_potential', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.pregnancytest', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.pregnancystatus'
