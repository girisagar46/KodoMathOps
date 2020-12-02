from django.contrib import admin

from kodomath.mathops.models import StudentStats, QuestionBank, QuestionTracker


@admin.register(StudentStats)
class StudentStatsAdmin(admin.ModelAdmin):
    list_display = ("user", "level", "average_time_to_answer")

    def average_time_to_answer(self, obj):
        from django.db.models import Avg

        result = QuestionTracker.objects.filter(
            student_stats__user=obj.user, student_stats=obj
        ).aggregate(Avg("time_to_answer"))
        return result["time_to_answer__avg"]


@admin.register(QuestionBank)
class QuestionBankAdmin(admin.ModelAdmin):
    pass


@admin.register(QuestionTracker)
class QuestionTrackerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student_stats",
        "question",
        "question_level",
        "time_to_answer_in_seconds",
    )

    def question(self, obj):
        return QuestionTracker.objects.filter(
            question_bank=obj.question_bank
        ).values_list("question_bank__question", flat=True)

    def time_to_answer_in_seconds(self, obj):
        return obj.time_to_answer.seconds

    def question_level(self, obj):
        return (
            QuestionTracker.objects.filter(question_bank=obj.question_bank)
            .values("question_bank__level")
            .distinct()
            .first()["question_bank__level"]
        )
