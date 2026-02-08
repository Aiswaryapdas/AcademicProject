from django.urls import path
from Admin import views
app_name='WAdmin'

urlpatterns = [
    path('faculty_reg/',views.faculty_register,name='faculty_register'),
    path('student_reg/',views.student_register,name='student_register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
]
