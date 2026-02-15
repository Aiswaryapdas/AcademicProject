from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('logout/', views.student_logout, name='logout'),
]
