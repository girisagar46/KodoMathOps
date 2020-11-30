from django.test import RequestFactory
from django.urls import reverse
from mock import patch
from rest_framework import status
from rest_framework.test import APITestCase

from kodomath.mathops.constants import MEDIUM_SCORE, BEGINNER_SCORE, ADVANCED_SCORE
from kodomath.mathops.models import QuestionTracker, QuestionBank, StudentStats, Level
from kodomath.mathops.test.factories import UserFactory
from kodomath.mathops.views import PlayView
from kodomath.users.models import User


class PlayViewGetTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.url = reverse("play")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        self.question_tracker_count = QuestionTracker.objects.count()

    def test_response_code(self):
        response = self.client.get(self.url)
        self.assertTrue(response.status_code == status.HTTP_201_CREATED)

    def test_response_message(self):
        response = self.client.get(self.url)
        self.assertTrue("id" in response.data.keys())
        self.assertTrue("question_bank" in response.data.keys())

    def test_question_tracker_created(self):
        self.client.get(self.url)
        self.assertEqual(
            QuestionTracker.objects.count(), self.question_tracker_count + 1
        )

    def test_latest_question_tracker_is_linked_with_other_models(self):
        self.client.get(self.url)
        question_tracker_obj: QuestionTracker = QuestionTracker.objects.all().order_by(
            "-created_at"
        ).first()
        self.assertFalse(question_tracker_obj.submitted)
        user = User.objects.get(pk=self.user.id)
        self.assertEqual(
            question_tracker_obj.student_stats.user.first_name, user.first_name
        )


class PlayViewPostTest(APITestCase):
    def setUp(self) -> None:
        self.user = UserFactory()
        self.url = reverse("play")
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.user.auth_token}")
        self.question_bank = QuestionBank.objects.first()
        self.student_stat = StudentStats.objects.get(user=self.user.id)
        self.question_tracker = QuestionTracker.objects.create(
            student_stats=self.student_stat, question_bank=self.question_bank
        )
        self.request_data_success = {
            "id": self.question_tracker.id,
            "submitted_result": "10",
        }
        self.request_data_failure = {
            "id": self.question_tracker.id,
            "submitted_result": "11",
        }

    def test_response_code(self):
        response = self.client.post(self.url, self.request_data_success)
        self.assertTrue(response.status_code == status.HTTP_202_ACCEPTED)

    def test_response_code_failed_evaluation(self):
        response = self.client.post(self.url, self.request_data_failure)
        self.assertTrue(response.status_code == status.HTTP_200_OK)

    def test_successful_evaluation_response(self):
        response = self.client.post(self.url, self.request_data_success)
        self.assertTrue(response.data)

    def test_unsuccessful_evaluation_response(self):
        response = self.client.post(self.url, self.request_data_failure)
        self.assertEqual(response.data["id"], str(self.question_tracker.id))

    @patch("kodomath.mathops.models.QuestionTracker.objects")
    def test_level_increment_beginner_to_medium(self, mock):
        mock.filter.return_value.count.return_value = BEGINNER_SCORE
        rf = RequestFactory()
        request = rf.post(self.url, self.request_data_failure)
        view = PlayView()
        view.request = request
        new_level = view.update_student_stats(
            self.student_stat.level, self.student_stat.user
        )
        self.assertEqual(new_level, Level.MEDIUM)

    @patch("kodomath.mathops.models.QuestionTracker.objects")
    def test_level_increment_medium_to_advanced(self, mock):
        mock.filter.return_value.count.return_value = MEDIUM_SCORE
        rf = RequestFactory()
        request = rf.post(self.url, self.request_data_failure)
        view = PlayView()
        view.request = request
        self.student_stat.level = Level.MEDIUM
        new_level = view.update_student_stats(
            self.student_stat.level, self.student_stat.user
        )
        self.assertEqual(new_level, Level.ADVANCED)

    @patch("kodomath.mathops.models.QuestionTracker.objects")
    def test_level_increment_advanced_to_complete(self, mock):
        mock.filter.return_value.count.return_value = ADVANCED_SCORE
        rf = RequestFactory()
        request = rf.post(self.url, self.request_data_failure)
        view = PlayView()
        view.request = request
        self.student_stat.level = Level.ADVANCED
        new_level = view.update_student_stats(
            self.student_stat.level, self.student_stat.user
        )
        self.assertEqual(new_level, Level.COMPLETED)
