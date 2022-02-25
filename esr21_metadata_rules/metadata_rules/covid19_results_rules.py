
from edc_constants.choices import NEG
from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register, P

app_label = 'esr21_subject'


@register()
class Covid19ResultsRule(CrfRuleGroup):

    covid_result = CrfRule(
        predicate=P('covid_result', 'eq', NEG),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[
            f'{app_label}.physicalexam',
            f'{app_label}.vaccinationdetails',
        ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.covid19results'
