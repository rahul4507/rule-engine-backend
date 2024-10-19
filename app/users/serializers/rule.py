from rest_framework import serializers
from users.models.rule import Rule


class RuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rule
        fields = ['id', 'rule_string', 'ast']