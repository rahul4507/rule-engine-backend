# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.rule import Rule
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..serializers.rule import RuleSerializer


class RuleCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RuleListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Rule.objects.all()
    serializer_class = RuleSerializer


class RuleDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Rule.objects.get(pk=pk)
        except Rule.DoesNotExist:
            return None

    def get(self, request, pk):
        rule = self.get_object(pk)
        if rule:
            serializer = RuleSerializer(rule)
            return Response(serializer.data)
        return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RuleSerializer(rule, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
