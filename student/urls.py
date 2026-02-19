from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('attendance/', views.student_attendance, name='attendance'),

    path('logout/', views.student_logout, name='logout'),
]
