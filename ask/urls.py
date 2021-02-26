from django.urls import path
from . import views

app_name = 'ask'
urlpatterns = [
    path('', views.question_list, name='question_list'),
    path('<int:pk>/', views.question_detail, name='question_detail'),
]
