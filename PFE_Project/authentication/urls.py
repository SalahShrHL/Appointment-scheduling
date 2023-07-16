from django.urls import path
from . import views

urlpatterns=[
    path('login/', views.Login, name="Login"),
    path('logout/', views.Logout, name="Logout"),
    path('Register/', views.RegisterP, name="RegisterP"),
    path('Register_doctor/', views.RegisterD, name="RegisterD"),
    path('LoginAdmin/', views.Login_admin, name="Login_admin")
]