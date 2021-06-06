from dateutil.relativedelta import relativedelta
from django.test import TestCase, tag
from edc_base.tests import SiteTestCaseMixin
from edc_base.utils import get_utcnow
from edc_constants.constants import YES, POS, NEG, FEMALE
from edc_facility.import_holidays import import_holidays
from edc_reference import LongitudinalRefset
from edc_reference.tests import ReferenceTestHelper

from .models import InformedConsent
from ..predicates import SubjectPredicates


class TestMaternalPredicates(SiteTestCaseMixin, TestCase):

    reference_helper_cls = ReferenceTestHelper
    app_label = 'esr21_metadata_rules'
    visit_model = 'esr21_subject.subjectvisit'
    reference_model = 'edc_reference.reference'

    @classmethod
    def setUpClass(cls):
        return super().setUpClass()

    def tearDown(self):
        super().tearDown()

    def setUp(self):
        self.subject_identifier = '111111111'

        InformedConsent.objects.create(
            subject_identifier=self.subject_identifier,
            gender=FEMALE)

        self.reference_helper = self.reference_helper_cls(
            visit_model=self.visit_model,
            subject_identifier=self.subject_identifier)

        report_datetime = get_utcnow()
        self.reference_helper.create_visit(
            report_datetime=report_datetime, timepoint='1000')

        import_holidays()

    def test_func_preg_no_prior_participation(self):
        pc = SubjectPredicates()
        pc.app_label = self.app_label

        self.assertTrue(
            pc.func_preg_no_prior_participation(self.maternal_visits[0],))

    @property
    def maternal_visits(self):
        return LongitudinalRefset(
            subject_identifier=self.subject_identifier,
            visit_model=self.visit_model,
            name=self.visit_model,
            reference_model_cls=self.reference_model
        ).order_by('report_datetime')
