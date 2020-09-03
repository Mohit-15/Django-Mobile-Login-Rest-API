from django.db import models
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator

# Create your models here.

class UserManager(BaseUserManager):
	def create_user(self, phone, password = None, is_staff = False, is_active= True, is_admin = False):
		if not phone:
			raise ValueError("User must have a phone number")
		if not password:
			raise ValueError("User must have a password")

		user_obj = self.model(
				phone = phone
			)
		user_obj.set_password(password)
		user_obj.is_staff = is_staff
		user_obj.is_admin = is_admin
		user_obj.is_active = is_active
		user_obj.save(using = self._db)
		return user_obj

	def create_superuser(self, phone, password = None):
		user = self.create_user(
				phone,
				password = password,
				is_staff = True,
				is_admin = True,
			)
		return user

class User(AbstractUser):
	username = None
	phone_regex = RegexValidator(regex = r'^\+?1?\d{9,14}$',
			message = "Phone number must be entered in the format: '+9999999999'. Upto 14 digits allowed"
		)
	phone = models.CharField(validators = [phone_regex], max_length = 15, unique = True)
	name = models.CharField(max_length = 30, blank = True, null = True)
	is_active = models.BooleanField(default = True)
	is_staff = models.BooleanField(default = False)
	is_admin = models.BooleanField(default = False)

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = []

	objects = UserManager()

	def __str__(self):
		return self.phone

	def has_perm(self, perm, obj=None):
		"Does the user have a specific permission?"
		return True

	def has_module_perms(self, app_label):
		"Does the user have permissions to view the app `app_label`?"
		return True

class OTPModel(models.Model):
	phone = models.CharField(max_length = 15)
	otp = models.CharField(max_length = 10, unique = True)
	count = models.IntegerField(default = 0, help_text = "Number of otp sent")
	validated = models.BooleanField(default = False)

	def __str__(self):
		return self.phone