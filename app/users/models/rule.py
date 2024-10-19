from django.db import models
from ..utils.rule_utils import ExpressionTree

class Rule(models.Model):
    rule_string = models.TextField(unique=True)
    ast = models.JSONField()

    def save(self, *args, **kwargs):
        self.ast = self.prepare_ast(self.rule_string)
        super().save(*args, **kwargs)

    def prepare_ast(self, rule_string):
        """Convert rule string to AST (nested dict)."""
        rule_tree = ExpressionTree(rule_string)
        return rule_tree.build_tree()

    def __str__(self):
        return self.rule_string
