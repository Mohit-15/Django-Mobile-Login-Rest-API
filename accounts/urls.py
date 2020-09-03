from . import views
from django.urls import path
from knox import views as knox_views

app_name = 'accounts'

urlpatterns = [
	path('validate', views.ValidatePhone.as_view(), name = 'validate'),
	path('validate_otp', views.ValidateOTP.as_view(), name = 'validate-otp'),
	path('register', views.RegisterUser.as_view(), name = 'register'),
	path('login', views.LoginViewAPI.as_view(), name = 'login'),
	path('logout', knox_views.LogoutView.as_view(), name = 'register'),
]
