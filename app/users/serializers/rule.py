from rest_framework import serializers
from ..models import Rule


class RuleSerializer(serializers.ModelSerializer):
    ast = serializers.ReadOnlyField()

    class Meta:
        model = Rule
        fields = ['id', 'rule_string', 'ast']