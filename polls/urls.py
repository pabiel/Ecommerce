from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('persons/', views.PersonList.as_view()),
    path('persons/<int:pk>/', views.PersonDetail.as_view()),
    path('persons/search/', views.GetByName.as_view()),
    path('teams/', views.team_list),
    path('teams/<int:pk>/', views.team_detail),
    path('teams/create/<int:pk>/', views.team_create_update_delete),
    path('teams/update/<int:pk>/', views.team_create_update_delete),
    path('teams/delete/<int:pk>/', views.team_create_update_delete),
]
urlpatterns = format_suffix_patterns(urlpatterns)
