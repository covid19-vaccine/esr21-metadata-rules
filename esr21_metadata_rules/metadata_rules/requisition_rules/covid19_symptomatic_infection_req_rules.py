from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register, P

from edc_constants.constants import YES
from edc_metadata import NOT_REQUIRED, REQUIRED
from esr21_labs.subject_panels import sars_pcr_panel

from ...predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


class Covid19SymptomaticInfectionsRuleGroup(RequisitionRuleGroup):

    sars_pcr = RequisitionRule(
        predicate=P('symptomatic_experiences', 'eq', YES),
        consequence=REQUIRED,
        alternative=NOT_REQUIRED,
        target_panels=[sars_pcr_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.covid19symptomaticinfections'
        requisition_model = f'{app_label}.subjectrequisition'
