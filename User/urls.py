from django.contrib import admin
from django.urls import path

from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.loginUser, name="login"),
	# path('register/', views.register, name="register"),
      # path('verify/<auth_token>', views.verify, name="verify"),
	path('logout/', views.logoutUser, name="logout"),

      path('change_password', views.change_password, name="change_password"),

	path('home/', views.home, name="home"),

	path('reset_password/', auth_views.PasswordResetView.as_view(template_name="User/restPassword/restPassword.html"), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name="User/restPassword/passwordRestSend.html"),
          name="password_reset_done"),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name="User/restPassword/newPssword.html"),
          name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name="User/restPassword/passwordResetComplete.html"),
          name="password_reset_complete"),
]
