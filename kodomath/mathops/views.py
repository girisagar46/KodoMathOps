import random
from datetime import datetime, timezone

from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from kodomath.mathops.constants import BEGINNER_SCORE, MEDIUM_SCORE, ADVANCED_SCORE
from kodomath.mathops.models import StudentStats, Level, QuestionBank, QuestionTracker
from kodomath.mathops.quiz_service import SubmissionEvaluator
from kodomath.mathops.serializers import QuestionTrackerSerializer


class PlayView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    @staticmethod
    def update_student_stats(player_level, user):
        level_attempt_count = QuestionTracker.objects.filter(
            question_bank__level=player_level, student_stats__user=user, submitted=True
        ).count()
        if player_level == Level.BEGINNER and level_attempt_count == BEGINNER_SCORE:
            player_level = Level.MEDIUM
        elif player_level == Level.MEDIUM and level_attempt_count == MEDIUM_SCORE:
            player_level = Level.ADVANCED
        elif player_level == Level.ADVANCED and level_attempt_count == ADVANCED_SCORE:
            player_level = Level.COMPLETED
        return player_level

    def get(self, *args, **kwargs):
        question_tracker = self.generate_question()
        serializer = QuestionTrackerSerializer(question_tracker)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def generate_question(self):
        student_stats = StudentStats.objects.get(user=self.request.user)
        question_bank_obj = random.choice(
            QuestionBank.objects.filter(level=student_stats.level)
        )
        question_tracker = QuestionTracker.objects.create(
            student_stats=student_stats, question_bank=question_bank_obj
        )
        return question_tracker
        # if QuestionTracker.objects.filter(question_bank=question_bank_obj, submitted=False).exists():
        #     print("cond1")
        #     return random.choice(QuestionTracker.objects.filter(submitted=False))
        # elif QuestionTracker.objects.filter(~Q(question_bank=question_bank_obj), submitted=True).exists():
        #     print("cond2")
        #     self.generate_question()
        # else:
        #     print("cond3")
        #     question_tracker = QuestionTracker.objects.create(student_stats=student_stats,
        #                                                       question_bank=question_bank_obj)
        #     return question_tracker

    def post(self, *args, **kwargs):
        submitted_answer = self.request.data
        question_obj = QuestionTracker.objects.get(id=submitted_answer["id"])
        expression = (
            f"{question_obj.question_bank.question['x']}"
            f"{question_obj.question_bank.question['operator']}"
            f"{question_obj.question_bank.question['y']}"
        )
        submission_evaluator = SubmissionEvaluator(
            expression, submitted_answer["submitted_result"]
        )
        evaluation = submission_evaluator.evaluate()
        if evaluation:
            question_obj.time_to_answer = (
                datetime.now(timezone.utc) - question_obj.created_at
            )
            question_obj.submitted = True
            question_obj.save()

            student_stat = StudentStats.objects.get(user=self.request.user)
            student_stat_level = PlayView.update_student_stats(
                student_stat.level, student_stat.user
            )
            student_stat.level = student_stat_level
            student_stat.save()

            return Response(evaluation, status=status.HTTP_202_ACCEPTED)
        else:
            serializer = QuestionTrackerSerializer(question_obj)
            return Response(serializer.data, status=status.HTTP_200_OK)
