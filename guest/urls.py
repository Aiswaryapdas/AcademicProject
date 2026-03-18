from django.urls import path
from guest import views
app_name='guest'

urlpatterns = [
    path('login/', views.login, name='guest_login'),
    path('', views.home, name='home'),
]
