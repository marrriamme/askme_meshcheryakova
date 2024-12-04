from django.urls import path
from django.contrib import admin
from app import views

urlpatterns = [
    path('', views.index, name='index'),
    path('hot/', views.hot, name='hot'),
    path('ask/', views.ask, name='ask'),
    path('login/', views.login, name='login'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.logout, name='logout'),
    path('question/<int:question_id>/', views.question, name='question'),
    path('tag/<str:tag_name>/', views.tag, name='tag'),  
]
