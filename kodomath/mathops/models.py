import uuid
from datetime import timedelta

from django.conf import settings
from django.db import models


class Level(models.IntegerChoices):
    BEGINNER = 1, "Beginner"
    MEDIUM = 2, "Medium"
    ADVANCED = 3, "Advanced"
    COMPLETED = 4, "Completed"


class StudentStats(models.Model):
    class Meta:
        """Meta."""

        db_table = "student_stats"
        verbose_name = "stats on each student"
        verbose_name_plural = "stats on each students"
        get_latest_by = "created_at"
        index_together = [["user", "level", "updated_at"]]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    level = models.PositiveIntegerField(
        "Level", default=Level.BEGINNER, choices=Level.choices
    )

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"{self.user.username} Level:{self.level}"


class QuestionBank(models.Model):
    class Meta:
        """Meta."""

        db_table = "question_bank"
        verbose_name = "questions categorized by level to show it to students"
        index_together = [["id", "level"]]

    id = models.IntegerField(primary_key=True, editable=False)
    level = models.PositiveIntegerField(
        "Level", default=Level.BEGINNER, choices=Level.choices
    )
    question = models.JSONField(verbose_name="question", blank=True, default=dict)

    def __str__(self):
        return f"{self.id}-level-{self.level}"


class QuestionTracker(models.Model):
    class Meta:
        """Meta."""

        db_table = "question_tracker"
        verbose_name = "track answers submitted by the students"
        index_together = [["id", "created_at"]]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student_stats = models.ForeignKey(StudentStats, on_delete=models.DO_NOTHING)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.DO_NOTHING)

    time_to_answer = models.DurationField(default=timedelta())
    submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return f"{self.id} [User:{self.student_stats.user}] [Level: {self.question_bank.level}]"
