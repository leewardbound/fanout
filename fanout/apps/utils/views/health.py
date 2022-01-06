from requests import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection


@api_view(["GET"])
def healthz(request):
    try:
        connection.ensure_connection()

    except Exception as e:
        return Response({"status": False, "details": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response({"status": True}, status=status.HTTP_200_OK)
