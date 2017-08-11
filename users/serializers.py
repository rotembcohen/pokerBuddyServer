from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id', 'username', 'email', 'venmo_username', 'phone_number', 'first_name', 'last_name')

