from edc_metadata import NOT_REQUIRED, REQUIRED
from edc_metadata_rules import CrfRule, CrfRuleGroup, register
from ..predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class AdverseEventRuleGroup(CrfRuleGroup):

    serious_ae = CrfRule(
        predicate=pc.func_serious_ae_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.seriousadverseevent', ])

    speical_interest_ae = CrfRule(
        predicate=pc.func_special_interest_ae_required,
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_models=[f'{app_label}.specialinterestadverseevent', ])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.adverseevent'
