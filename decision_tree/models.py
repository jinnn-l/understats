from django.db import models
from django.db.models import Q, F

class DecisionTreeNode(models.Model):
    class NodeType(models.TextChoices):
        ROOT = 'root',
        INTERNAL = 'internal',
        TERMINAL = 'terminal'

    node_id = models.IntegerField(primary_key = True) #primary key: integer id
    node_type = models.CharField(choices = NodeType.choices) #either root, internal, or terminal node
    node_text = models.TextField() #text description

    def __str__(self):
        return str(self.node_id) + '. ' + str(self.node_text)

class DecisionTreeChoice(models.Model):
    #only defined by its contents, can be shared among paths
    choice_text = models.TextField(primary_key = True)

class DecisionTreePath(models.Model):
    #uniquely defined by start node (vertex), end node (vertex), AND choice (edge)
    start_node = models.ForeignKey(DecisionTreeNode, on_delete = models.CASCADE, related_name = 'start_node')
    end_node = models.ForeignKey(DecisionTreeNode, on_delete = models.CASCADE, related_name = 'end_node')
    choice = models.ForeignKey(DecisionTreeChoice, on_delete = models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                check = ~Q(start_node = F('end_node')),
                name = 'node_not_linked_to_self'
            ),
            models.UniqueConstraint(
                fields = ['start_node', 'end_node'],
                name = 'only_one_path_between_two_nodes'
            ),
        ]