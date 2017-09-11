from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True)
	
	def create(self, validated_data):

		user = User.objects.create(
			**validated_data
		)
		user.set_password(validated_data['password'])
		user.save()

		return user

	class Meta:
		model = User
		fields = ('id','password','username','venmo_username','first_name',
			'last_name','picture_url','facebook_token','push_token',
			'default_min_bet','buy_in_intervals','chip_basic_unit')
		
		extra_kwargs = {'password': {'write_only': True}}

class UserMinimalSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('id','username','venmo_username','first_name','last_name','picture_url')


class UserPaymentSerializer(serializers.ModelSerializer):

	class Meta:
		model = User
		fields = ('venmo_username','first_name','last_name')