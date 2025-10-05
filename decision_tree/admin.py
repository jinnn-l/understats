from django.contrib import admin

from .models import DecisionTreeNode, DecisionTreeChoice, DecisionTreePath

admin.site.register(DecisionTreeNode)
admin.site.register(DecisionTreeChoice)
admin.site.register(DecisionTreePath)