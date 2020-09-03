from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions
from .models import User, OTPModel
from django.shortcuts import get_object_or_404
import random
from .serializers import OTPRegisterSerializer, LoginSerializer
from knox.views import LoginView as knoxLoginView
from knox.auth import TokenAuthentication
from django.contrib.auth import login

# Create your views here.

class ValidatePhone(APIView):
	def post(self, request, *args, **kwargs):
		phone_number = request.data.get('phone')
		if phone_number:
			phone = str(phone_number)
			user = User.objects.filter(phone = phone)
			if user.exists():
				return Response({
						'status': False,
						'message': 'User already exist'
					})
			else:
				key = send_otp(phone)
				if key:
					old_data = OTPModel.objects.filter(phone = phone)
					if old_data.exists():
						old_data = old_data.first()
						count = old_data.count
						if count > 10:
							return Response({
								'status': False,
								'message': 'Limit Exceed'
							})		
						old_data.count = count+1
						old_data.save()
						print("Count: {}".format(count))
						return Response({
								'status': True,
								'message': 'OTP send successfully'
							})
					else:	
						otp_obj = OTPModel(phone = phone, otp = key)
						otp_obj.save()
						return Response({
								'status': True,
								'message': 'OTP send successfully'
							})
				else:
					return Response({
							'status': False,
							'message': 'Internal Error'
						})
		else:
			return Response({
						'status': False,
						'message': 'Phone number is not given'
					})

class ValidateOTP(APIView):
	def post(self, request, *args, **kwargs):
		phone = request.data.get('phone', False)
		otp_send = request.data.get('otp', False)

		if phone and otp_send:
			old = OTPModel.objects.filter(phone = phone)
			if old.exists():
				old = old.first()
				otp = old.otp
				if str(otp_send) == str(otp):
					old.validated = True
					old.save()
					return Response({
							'status': True,
							'message': "OTP Matched..Account verified successfully"
						})
				else:
					return Response({
							'status': False,
							'message': "OTP does not match"
						})
			else:
				return Response({
							'status': False,
							'message': "User does not exist.. First validate Phone"
						})
		else:
			return Response({
							'status': False,
							'message': "Both inputs are missing??"
						})

class RegisterUser(APIView):
	def post(self, request, *args, **kwargs):
		phone = request.data.get('phone', False)
		password = request.data.get('password', False)

		if phone and password:
			old = OTPModel.objects.filter(phone = phone)
			if old.exists():
				old = old.first()
				valid = old.validated
				if valid:
					test_data = {
						'phone': phone,
						'password':password,
					}
					serialize = OTPRegisterSerializer(data = test_data)
					serialize.is_valid(raise_exception = True)
					serialize.save()
					old.delete()
					return Response({
							'status': True,
							'message': "Account created"
						})	
				else:
					return Response({
							'status': False,
							'message': "Mobile is not validated"
						})	
			else:
				return Response({
							'status': False,
							'message': "User have to verify first"
						})
		else:
			return Response({
							'status': False,
							'message': "Both inputs are missing??"
						})

class LoginViewAPI(knoxLoginView):
	permission_classes = (permissions.AllowAny,)

	def post(self, request, format = None):
		serializer = LoginSerializer(data = request.data)
		serializer.is_valid(raise_exception = True)
		user = serializer.validated_data['user']
		login(request, user)
		return super().post(request, format= None)

def send_otp(phone):
	if phone:
		key = random.randint(999,9999)
		print(key)
		return key
	else:
		return False