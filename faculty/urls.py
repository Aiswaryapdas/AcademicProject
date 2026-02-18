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

    path('logout/', views.logout_view, name='logout'),
]
