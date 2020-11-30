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
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.DO_NOTHING)
    level = models.PositiveIntegerField(
        "Level", default=Level.BEGINNER, choices=Level.choices
    )

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)


class QuestionBank(models.Model):
    id = models.IntegerField(primary_key=True, editable=False)
    level = models.PositiveIntegerField(
        "Level", default=Level.BEGINNER, choices=Level.choices
    )
    question = models.JSONField(verbose_name="question", blank=True, default=dict)


class QuestionTracker(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student_stats = models.ForeignKey(StudentStats, on_delete=models.DO_NOTHING)
    question_bank = models.ForeignKey(QuestionBank, on_delete=models.DO_NOTHING)

    time_to_answer = models.DurationField(default=timedelta())
    submitted = models.BooleanField(default=False)

    created_at = models.DateTimeField(editable=False, auto_now_add=True)
    updated_at = models.DateTimeField(editable=False, auto_now=True)
