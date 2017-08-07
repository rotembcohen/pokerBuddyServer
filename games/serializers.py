from rest_framework import serializers

from games.models import Game, Bet
from users.models import User

class GameSerializer(serializers.HyperlinkedModelSerializer):

	bets = serializers.StringRelatedField(many=True,read_only=True,allow_empty=True)

	identifier = serializers.CharField(required=False,read_only=True)
	host = serializers.StringRelatedField(
		required=False
	)

	class Meta:
		model = Game
		fields = '__all__'
		lookup_field = 'identifier'
		extra_kwargs = {
			'url': {'lookup_field': 'identifier'}
		}
