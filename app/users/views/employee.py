from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models import Employee, Rule
from ..serializers.employee import EmployeeSerializer
from core.rule import ExpressionTree


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by("-id")
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination


class EmployeeEvaluateAPIView(APIView):

    def post(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            data = serializer.data
            rule_id = request.data.get('rule')
            rule_object = Rule.objects.get(pk=rule_id)
            ast_json = rule_object.ast
            ast = ExpressionTree(ast=ast_json, data=data)
            result = ast.evaluate()
            if result:
                return Response({"result":"pass", "status":True}, status=status.HTTP_200_OK)
            else:
                return Response({"result":"Fail", "status":False}, status=status.HTTP_200_OK)

        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Rule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)