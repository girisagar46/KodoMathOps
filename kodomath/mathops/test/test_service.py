from django.test import TestCase

from kodomath.mathops.quiz_service import SubmissionEvaluator


class TestSubmissionEvaluatorTestCase(TestCase):
    """
    Tests SubmissionEvaluator service operations.
    """

    def setUp(self):
        self.data = [
            {"expression": "3 + 7", "submitted": "10"},
            {"expression": "3 - 7", "submitted": "-4"},
            {"expression": "3 * 7", "submitted": "21"},
            {"expression": "3 / 3", "submitted": "1"},
            {"expression": "11 + 7", "submitted": "18"},
            {"expression": "0 - 17", "submitted": "-17"},
            {"expression": "17 * 7", "submitted": "119"},
            {"expression": "0 / 17", "submitted": "0"},
            {"expression": "1.52 + 2.31", "submitted": "3.83"},
            {"expression": "1.5 - 3.4", "submitted": "-1.9"},
            {"expression": "2.31 * 3.51", "submitted": "8.1"},
            {"expression": "8.45 / 2", "submitted": "4.22"},
        ]

    def test_one_true_evaluation(self):
        evaluator = SubmissionEvaluator(expression="4*4", submitted_result="16")
        self.assertTrue(evaluator.evaluate())

    def test_false_evaluation(self):
        evaluator = SubmissionEvaluator(
            expression="2.31 * 3.51", submitted_result="8.10"
        )
        self.assertFalse(evaluator.evaluate())

    def test_evaluate(self):
        for each in self.data:
            evaluator = SubmissionEvaluator(
                expression=each["expression"], submitted_result=each["submitted"]
            )
            with self.subTest():
                self.assertTrue(evaluator.evaluate())
