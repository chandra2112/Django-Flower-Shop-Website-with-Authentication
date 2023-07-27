from django.urls import path
from . import views

urlpatterns = [
    path("",views.home, name="home"),
    path("login",views.login, name="login"),
    path("register",views.register, name="register"),
    path("logout_user",views.logout_user, name="logout"),
    path('send-otp-email/', views.send_otp_email, name='send_otp_email'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('set-new-password/', views.set_new_password, name='set_new_password'),
    
]
