from rest_framework import serializers
from users.models import User

class UserSerializer(serializers.ModelSerializer):

	password = serializers.CharField(write_only=True)
	profit = serializers.DecimalField(max_digits=12, decimal_places=2,read_only=True)
	
	def create(self, validated_data):

		user = User.objects.create(
			**validated_data
		)
		user.set_password(validated_data['password'])
		user.save()

		return user

	class Meta:
		model = User
		fields = ('id','password','username','email','venmo_username','phone_number','first_name',
			'last_name','picture_url','facebook_token','push_token','profit')
		extra_kwargs = {'password': {'write_only': True}}