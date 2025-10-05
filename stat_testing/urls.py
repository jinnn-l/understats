from django.urls import path
from stat_testing.views import upload_file

app_name = 'stat_testing'
urlpatterns = [
    path('', upload_file, name = 'stat_testing'),
]