from unittest import TestCase

from django.urls import resolve, reverse

from kodomath.mathops.views import PlayView


class QuestionAPIUrlResolveTest(TestCase):
    """Test cases for PlayView Urls."""

    def setUp(self) -> None:
        self.url = reverse("play")

    def test_get_endpoint(self):
        self.assertEqual(self.url, "/api/v1/mathops/play/")

    def test_urls_user_count(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__module__, PlayView.as_view().__module__)
        self.assertEqual(found.func.__name__, PlayView.as_view().__name__)
