from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginView, name='login'),
    path('logout/', views.logoutView, name='logout'),
    path('register/', views.registerView, name='register'),
    
    path('', views.profiles, name='profiles'),
    path('profile/<str:pk>/', views.userProfile, name='user-profile'),
    
    path('account/', views.userAccount, name='account'),
    path('update-account/', views.updateAccount, name='update-account'),
    
    path('create-skill/', views.createSkill, name='create-skill'),
    path('update-skill/<str:pk>/', views.updateSkill, name='update-skill'),
    path('delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
    
    path('inbox/', views.inboxView, name='inbox'),
    path('message/<str:pk>/', views.messageView, name='message'),
    path('create-message/<str:pk>', views.createMessage, name='create-message'),
    path('delete-message/<str:pk>', views.deleteMessage, name='delete-message'),
]
