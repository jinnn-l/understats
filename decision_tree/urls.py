from django.contrib import admin
from django.urls import include, path
from decision_tree.views import decision_tree_view

app_name = 'decision_tree'
urlpatterns = [
    path('', decision_tree_view, name = 'decision_tree'),
]