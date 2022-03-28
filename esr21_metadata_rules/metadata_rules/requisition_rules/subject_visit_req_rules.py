from edc_metadata_rules import RequisitionRule, RequisitionRuleGroup, register
from edc_metadata import NOT_REQUIRED, REQUIRED
from esr21_labs.subject_panels import sars_pcr_panel

from ...predicates import SubjectPredicates

app_label = 'esr21_subject'
pc = SubjectPredicates()


@register()
class SubjectVisitReqRuleGroup(RequisitionRuleGroup):

    sars_pcr_enroll = RequisitionRule(
        predicate=pc.func_symptomatic_infection_pcr_enrol,
        consequence=NOT_REQUIRED,
        alternative=REQUIRED,
        target_panels=[sars_pcr_panel])

    class Meta:
        app_label = app_label
        source_model = f'{app_label}.subjectvisit'
        requisition_model = f'{app_label}.subjectrequisition'
