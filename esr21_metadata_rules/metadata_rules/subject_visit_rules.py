from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
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

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.subjectvisit'
