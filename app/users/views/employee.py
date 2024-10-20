from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from ..models import Employee, Rule
from ..serializers.employee import EmployeeSerializer
from ..utils.rule_utils import ExpressionTree


class EmployeeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Retrieve a list of employees or a single employee by ID."""
        try:
            employee = Employee.objects.all()
            serializer = EmployeeSerializer(employee, many=True)
            return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        """Create a new employee record."""
        try:
            data = request.data
            serializer = EmployeeSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"result":serializer.data}, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        """Update an existing employee record."""
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"result":serializer.data}, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        """Delete an employee record."""
        try:
            employee = Employee.objects.get(pk=pk)
            employee.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class EmployeeDetailAPIView(APIView):

    def get(self, request, pk):
        try:
            employee = Employee.objects.get(pk=pk)
            serializer = EmployeeSerializer(employee)
            return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

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