from django.urls import path
from . import views

app_name = 'ask'
urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
    path('create/', views.create_question, name='create_question'),
    path('<int:pk>/edit/', views.edit_question, name='edit_question'),
    path('<int:pk>/delete/', views.delete_question, name='delete_question'),
    path('<int:pk>/delete/confirm',
         views.confirm_delete_question,
         name='confirm_delete_question'),
    path('delete/success/',
         views.delete_question_done,
         name='delete_question_done'),
    path('<int:pk>/create_answer/', views.create_answer, name='create_answer'),
    path('answer/<int:pk>/edit/', views.edit_answer, name='edit_answer'),
    path('answer/<int:pk>/delete/', views.delete_answer, name='delete_answer'),
    path('answer/<int:pk>/delete/confirm',
         views.confirm_delete_answer,
         name='confirm_delete_answer'),
    path('<int:pk>/answer/delete/success/',
         views.delete_answer_done,
         name='delete_answer_done')
]
