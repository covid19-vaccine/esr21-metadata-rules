from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register, P

from edc_constants.constants import IND
from edc_metadata import NOT_REQUIRED, REQUIRED
from esr21_labs.subject_panels import urine_hcg_panel

from ...predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class PregnancyTestRuleGroup(RequisitionRuleGroup):

    urine_hcg = RequisitionRule(
        predicate=P('result', 'eq', IND),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[urine_hcg_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.pregnancytest'
        requisition_model = f'{app_label}.subjectrequisition'
