from django.urls import path
from . import views

app_name = 'gallery'

urlpatterns = [
    path('upload/', views.CSVImportView.as_view(), name='upload'),
    path('list/', views.LandscapeListView.as_view(), name='list'),
]