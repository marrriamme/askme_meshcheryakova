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
    path('<int:question_id>/like_question', views.like_question, name = 'like_question'),
    path('<int:answer_id>/like_answer', views.like_answer, name = 'like_answer'),
    path('<int:question_id>/dislike_question', views.dislike_question, name = 'dislike_question'),
    path('<int:answer_id>/dislike_answer', views.dislike_answer, name = 'dislike_answer'),
]
