from django.urls import path
from faculty import views

app_name = 'faculty'

urlpatterns = [
    path('dashboard/', views.homepage, name='homepage'),
    path('logout/', views.logout_view, name='logout'),
]
