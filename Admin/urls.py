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
    path('review-schedule/', views.review_schedule, name='review_schedule'),
    path('review-schedule/add/', views.review_schedule_add, name='review_schedule_add'),
    path('review-schedule/edit/<int:id>/', views.review_schedule_edit, name='review_schedule_edit'),
    path('review-schedule/delete/<int:id>/', views.review_schedule_delete, name='review_schedule_delete'),
    path('project-groups/', views.view_project_groups, name='view_project_groups'),
    path('faculty/review-schedule/', views.faculty_review_schedule, name='faculty_review_schedule'),
    path('student/review-schedule/', views.student_review_schedule, name='student_review_schedule'),
    path('view-submissions/', views.admin_view_submissions, name='admin_view_submissions'),
    # DOCUMENT SCHEDULE
path('document-schedule/', views.document_schedule, name='document_schedule'),
path('document-schedule/add/', views.document_schedule_add, name='document_schedule_add'),
path('document-schedule/edit/<int:id>/', views.document_schedule_edit, name='document_schedule_edit'),
path('document-schedule/delete/<int:id>/', views.document_schedule_delete, name='document_schedule_delete'),
 path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('attendance/', views.admin_attendance, name='admin_attendance'),




]
