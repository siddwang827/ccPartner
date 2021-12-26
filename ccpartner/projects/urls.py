from django.urls import path
from . import views

urlpatterns = [
    path('', views.projects, name='projects'),
    path('project/<str:pk>/', views.project, name='project'),
    path('create-project/', views.createProject, name='create-project'),
    path('update-project/<str:pk>/', views.updateProject, name="update-project"),
    path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),

    path('remove-member/<str:pk>/', views.removeMember, name='remove-member'),
    path('quit-team/', views.quitTeam, name="quit-team"),

    path('apply/<str:pk>/', views.apply, name='apply'),
    path('apply-box/', views.applyBox, name='apply-box'),
    path('verify-apply/<str:pk>', views.verifyApply, name='verify-apply'),
]

