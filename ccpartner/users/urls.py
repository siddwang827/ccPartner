from django.urls import path
from . import views

urlpatterns = [
    path('login', views.loginUser, name='login'),
    path('logout', views.logoutUser, name='logout'),
    path('register', views.registerUser, name='register'),
    
    
    path('', views.profiles, name='profiles'),
    path('user-profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-profile/', views.updateProfile,  name='update-profile'),
    
    path('account/', views.userAccount, name='account'),


    path('create-hobby/', views.createHobby, name='create-hobby'),
    path('update-hobby/<str:pk>/', views.updateHobby, name='update-hobby'),    
    path('delete-hobby/<str:pk>/', views.deleteHobby, name='delete-hobby'),

    
]