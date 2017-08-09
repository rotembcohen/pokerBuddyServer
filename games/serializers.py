from rest_framework import serializers

from games.models import Game, Bet
from users.models import User
from users.serializers import UserSerializer

class BetSerializer(serializers.ModelSerializer):

	player = UserSerializer(read_only=True)
	game = serializers.StringRelatedField(read_only=True)

	class Meta:
		model = Bet
		fields = '__all__'


class GameSerializer(serializers.ModelSerializer):

	bets = BetSerializer(many=True,read_only=True,allow_empty=True)

	identifier = serializers.CharField(required=False,read_only=True)
	host = serializers.PrimaryKeyRelatedField(
		required=False
	)

	class Meta:
		model = Game
		fields = '__all__'
		lookup_field = 'identifier'
		extra_kwargs = {
			'url': {'lookup_field': 'identifier'}
		}
