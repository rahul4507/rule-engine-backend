from rest_framework import serializers
from ..models import Rule


class RuleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rule
        fields = ['id', 'rule_string', 'name', 'description', 'ast', 'created_date']