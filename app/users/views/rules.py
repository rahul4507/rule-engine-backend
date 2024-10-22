# views.py
from rest_framework import status, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from ..models.rule import Rule
from rest_framework.permissions import IsAuthenticated
from ..serializers.rule import RuleSerializer
from core.rule import ExpressionTree

class RuleViewSet(viewsets.ModelViewSet):
    queryset = Rule.objects.all().order_by('-created_date')
    serializer_class = RuleSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = LimitOffsetPagination

    def create(self, request, *args, **kwargs):
        data = request.data.copy()
        ast = ExpressionTree(data.get('rule_string')).build_tree()
        data['ast'] = ast
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response({"result": serializer.data}, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        rule = self.get_object()
        data = request.data.copy()
        ast = ExpressionTree(data.get('rule_string')).build_tree()
        data['ast'] = ast
        serializer = self.get_serializer(rule, data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response({"result": serializer.data}, status=status.HTTP_200_OK)


class CombineRulesAPIView(APIView):
    def post(self, request):
        try:
            rule_ids = request.data.get('rules', [])

            if not rule_ids:
                return Response({"error": "No rule IDs provided."}, status=status.HTTP_400_BAD_REQUEST)

            rules = Rule.objects.filter(id__in=rule_ids)

            if len(rules) < 2:
                return Response({"error": "You must provide at least two rules to combine."},
                                status=status.HTTP_400_BAD_REQUEST)
            asts = [rule.ast for rule in rules]
            combined_ast = ExpressionTree()
            combined_ast.combine_multiple_asts(asts)
            combined_rule_string = combined_ast.inorder()
            combined_ast_dict = combined_ast.ast
            new_rule_name = "Combined Rules"
            for r in rules:
                 new_rule_name = new_rule_name +f"-{r.name}"
            description = "combined the rules."
            data = {
                "name": new_rule_name,
                "description":description,
                "ast": combined_ast_dict,
                "rule_string": combined_rule_string
            }
            serializer = RuleSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Rule.DoesNotExist:
            return Response({"error": "Rule not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
