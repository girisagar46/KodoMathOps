from rest_framework import serializers

from .models import QuestionTracker, QuestionBank


class QuestionBankSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionBank
        fields = (
            "level",
            "question",
        )
        read_only_fields = ("id",)


class QuestionTrackerSerializer(serializers.ModelSerializer):
    question_bank = QuestionBankSerializer(many=False, read_only=True)

    class Meta:
        model = QuestionTracker
        fields = (
            "id",
            "question_bank",
        )
        read_only_fields = ("id",)
