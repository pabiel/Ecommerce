from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('persons/', views.person_list),
    path('persons/<int:pk>/', views.person_detail),
    path('persons/search/', views.get_by_names),
    path('teams/', views.team_list),
    path('teams/<int:pk>/', views.team_detail),
]
urlpatterns = format_suffix_patterns(urlpatterns)
