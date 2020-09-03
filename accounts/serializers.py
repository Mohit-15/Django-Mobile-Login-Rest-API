from rest_framework import serializers
from .models import User
from django.contrib.auth import authenticate

class OTPRegisterSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('phone',)

		def create(self, validated_data):
			usr = User.objects.create_user(**validated_data)
			return usr

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('phone','name',)

class LoginSerializer(serializers.Serializer):
	phone = serializers.CharField()
	password = serializers.CharField(
			style = {'input_type': 'password',}
		)

	def validate(self, data):
		print(data)
		phone = data.get('phone')
		password = data.get('password')

		if phone and password:
			if User.objects.filter(phone = phone).exists():
				print(phone, password)
				user = authenticate(request = self.context.get('request'), phone = phone, password = password)
				print(user)

			else:
				msg = {
					'status': False,
					'message': 'Phone number not exist'
				}
				raise serializers.ValidationError(msg)

			if not user:
				msg = {
					'status': False,
					'message': 'Phone number and password do not match'
				}
				raise serializers.ValidationError(msg, code = 'authentication')
		else:
			msg = {
					'status': False,
					'message': 'Phone number and password not found'
				}
			raise serializers.ValidationError(msg, code = 'authentication')

		data['user'] = user
		return data