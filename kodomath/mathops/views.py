from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class BaseView(APIView):
    authentication_classes = [
        TokenAuthentication,
    ]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        return Response(status=status.HTTP_200_OK)
