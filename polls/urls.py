from django.urls import path, include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('persons/', views.person_list),
    path('persons/<int:pk>/', views.person_detail),
    path('persons/search/', views.get_by_names),
    path('persons/create/<int:pk>/', views.person_create),
    path('persons/update/<int:pk>/', views.person_update),
    path('persons/delete/<int:pk>/', views.person_delete),
    path('teams/', views.team_list),
    path('teams/<int:pk>/', views.team_detail),
    path('teams/create/<int:pk>/', views.team_create),
    path('teams/update/<int:pk>/', views.team_update),
    path('teams/delete/<int:pk>/', views.team_delete),
    # path('users/', views.UserList.as_view()),
    path('teams/<int:pk>/members', views.teams_members),
    path('persons/<int:pk>/details', views.person_view),
    path('persons/<int:pk>/team_members', views.person_team_members),
    # path('users/<int:pk>/', views.UserDetail.as_view()),
    # path('login/', include('rest_framework.urls')),
]
urlpatterns = format_suffix_patterns(urlpatterns)
