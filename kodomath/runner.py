from django_nose import NoseTestSuiteRunner
from django_nose.runner import BaseRunner


class TestSuiteRunner(NoseTestSuiteRunner):
    django_opts = BaseRunner.django_opts + ["-k"]

    def setup_databases(self):
        """Using current db for testing"""

    def teardown_databases(self, *args, **kwargs):
        pass
