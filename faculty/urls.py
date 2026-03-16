from django.urls import path
from faculty import views

app_name = 'faculty'

urlpatterns = [
    path('dashboard/', views.homepage, name='homepage'),
    path('view-submissions/<int:schedule_id>/',
     views.faculty_view_submissions,
     name='view_submissions'),

path('add-mark/<int:submission_id>/',
     views.add_mark,
     name='add_mark'),
     path('attendance/', views.attendance_mark, name='attendance_mark'),
     path('add_review_marks/<int:review_id>/',views.add_review_marks,name='add_review_marks'),
     path('faculty/documents/', views.faculty_document_view, name='faculty_document_view'),
      path('documents/', views.document_schedule_list, name='document_schedules'),
    path('documents/<int:schedule_id>/', views.schedule_submissions, name='schedule_submissions'),
    path('logout/', views.logout_view, name='logout'),
]
