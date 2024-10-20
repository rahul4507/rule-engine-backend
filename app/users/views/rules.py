# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.rule import Rule
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from ..serializers.rule import RuleSerializer
from ..utils.rule_utils import ExpressionTree


class RuleAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        try:
            return Rule.objects.get(pk=pk)
        except Rule.DoesNotExist:
            return None

    def post(self, request):
        data  = request.data.copy()
        ast = ExpressionTree(data.get('rule_string')).build_tree()
        data['ast'] = ast
        serializer = RuleSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result":serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data.copy()
        ast = ExpressionTree(data.get('rule_string')).build_tree()
        data['ast'] = ast
        serializer = RuleSerializer(rule, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        rule = self.get_object(pk)
        if not rule:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        rule.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


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
            return Response({"result":serializer.data}, status=status.HTTP_200_OK)
        return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)


class CombineRulesAPIView(APIView):
    def post(self, request):
        try:
            rule_ids = request.data.get('rule_ids', [])

            if not rule_ids:
                return Response({"error": "No rule IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

            rules = Rule.objects.filter(id__in=rule_ids)

            if len(rules) < 2:
                return Response({"error": "You must provide at least two rules to combine."},
                                status=status.HTTP_400_BAD_REQUEST)
            combined_rule_string = ' AND '.join([rule.rule_string for rule in rules])
            combined_ast = ExpressionTree(combined_rule_string)
            combined_ast.combine_rules()

            new_rule_name = "Combined Rule"
            data = {
                "name": new_rule_name,
                "ast": combined_ast,
                "rule_string": combined_rule_string
            }
            serializer = RuleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def combine_asts(self, ast_dicts):
        """
        Combines the AST dictionaries into a single one by combining them using 'AND'.
        Modify the operator to 'OR' if needed.
        """
        if len(ast_dicts) == 1:
            return ast_dicts[0]  # If only one rule, return it directly

        combined_ast = {
            "val": "AND",  # Change to 'OR' if needed
            "left": ast_dicts[0],  # First rule AST as the left child
            "right": self.combine_asts(ast_dicts[1:])  # Recursively combine the rest of the ASTs
        }

        return combined_ast