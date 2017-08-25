from rest_framework import serializers

from games.models import Game, Bet, Payment
from users.models import User
from users.serializers import UserSerializer

class PaymentSerializer(serializers.ModelSerializer):

	source = UserSerializer(read_only=True)
	target = UserSerializer(read_only=True)

	class Meta:
		model = Payment
		fields = '__all__'

class BetSerializer(serializers.ModelSerializer):

	player = UserSerializer(read_only=True)
	game = serializers.StringRelatedField(read_only=True)
	payments = PaymentSerializer(many=True,read_only=True,allow_empty=True)

	class Meta:
		model = Bet
		fields = '__all__'


class GameSerializer(serializers.ModelSerializer):

	bets = BetSerializer(many=True,read_only=True,allow_empty=True)

	identifier = serializers.CharField(required=False,read_only=True)
	host = serializers.PrimaryKeyRelatedField(
		required=False,
		read_only=True
	)

	class Meta:
		model = Game
		fields = '__all__'
		lookup_field = 'identifier'
		extra_kwargs = {
			'url': {'lookup_field': 'identifier'}
		}
