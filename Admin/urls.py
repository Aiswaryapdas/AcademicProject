from django.urls import path
from Admin import views
app_name='WAdmin'

urlpatterns = [
    path('faculty_reg/',views.faculty_register,name='faculty_register'),
    path('student_reg/',views.student_register,name='student_register'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('faculty-list/', views.faculty_list, name='faculty_list'),
path('student-list/', views.student_list, name='student_list'),
path('project-group-list/', views.project_group_list, name='project_group_list'), 
path('delete-student/<int:id>/', views.delete_student, name='delete_student'),
    path('create-group/', views.create_project_group, name='create_project_group'),
    path('review-schedule/', views.review_schedule, name='review_schedule'),
    path('review-schedule/add/', views.review_schedule_add, name='review_schedule_add'),
    path('review-schedule/edit/<int:id>/', views.review_schedule_edit, name='review_schedule_edit'),
    path('review-schedule/delete/<int:id>/', views.review_schedule_delete, name='review_schedule_delete'),
    path('project-groups/', views.view_project_groups, name='view_project_groups'),
    path('faculty/review-schedule/', views.faculty_review_schedule, name='faculty_review_schedule'),
    path('student/review-schedule/', views.student_review_schedule, name='student_review_schedule'),
   
 path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('attendance/', views.admin_attendance, name='admin_attendance'),
      path('semester-attendance/', views.semester_attendance_view, name='semester_attendance'),
      path('view_review_marks/', views.admin_view_review_marks, name='view_review_marks'),
      path('add_document_schedule/', views.add_document_schedule, name='add_document_schedule'),
      path('document_schedule_list/', views.document_schedule_list, name='document_schedule_list'),
      path('edit_document_schedule/<int:id>/', views.edit_document_schedule, name='edit_document_schedule'),
path('delete_document_schedule/<int:id>/', views.delete_document_schedule, name='delete_document_schedule'),

    path('document-submissions/', views.admin_view_document_submissions, name='admin_document_submissions'),

path('documents/', views.admin_document_schedules, name='admin_document_schedules'),
path('documents/<int:schedule_id>/', views.admin_schedule_submissions, name='admin_schedule_submissions'),

 path('logout/', views.admin_logout, name='admin_logout'),
 path('students/', views.view_students, name='view_students'),
 path('bca-proposals/', views.view_bca_proposals, name='bca_proposals'),
path('mca-proposals/', views.view_mca_proposals, name='mca_proposals'),
path('approve/<int:id>/', views.approve_proposal, name='approve_proposal'),
path('reject/<int:id>/', views.reject_proposal, name='reject_proposal'),
path('add-notice/', views.add_notice, name='add_notice'),
path('notice-board/', views.notice_board, name='notice_board'),
path('manage-notices/', views.admin_notice_list, name='admin_notice_list'),
path('edit-notice/<int:id>/', views.edit_notice, name='edit_notice'),
path('delete-notice/<int:id>/', views.delete_notice, name='delete_notice'),
]
