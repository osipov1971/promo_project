from django.urls import path
from .views import *

urlpatterns = [
    path('language/', LanguageListView.as_view({'get': 'list'}))
]