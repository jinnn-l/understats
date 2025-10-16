from django.urls import path
from stat_testing.views import *

app_name = 'stat_testing'
urlpatterns = [
    path('', UploadFileView.as_view()),
    path('details/', RequestAttributeView.as_view()),
    path('results/', DisplayResultsView.as_view()),
]