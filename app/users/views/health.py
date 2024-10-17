from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from users import logger


class HealthCheckAPIView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        logger.info("logger started")
        return Response({"msg": "Healthy like a thor!!"})
