from django.urls import path
from Admin import views
app_name='WAdmin'

urlpatterns = [
    path('faculty_reg/',views.faculty_register,name='faculty_register'),
    path('student_reg/',views.student_register,name='student_register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty_list/', views.faculty_list, name='faculty_list'), 
    path('student_list/', views.student_list, name='student_list'), 
    path('create-group/', views.create_project_group, name='create_project_group'),

]
