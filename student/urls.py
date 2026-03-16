from django.urls import path
from student import views

app_name = 'student'

urlpatterns = [
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('view_marks/', views.view_my_marks, name='view_marks'),
    path('student_documents/', views.student_document_list, name='student_document_list'),

    path('upload_document/<int:id>/', views.upload_document, name='upload_document'),
    path('document-marks/', views.student_document_marks, name='student_document_marks'),

    path('logout/', views.student_logout, name='logout'),
]
