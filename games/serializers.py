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

class BetSerializer(serializers.HyperlinkedModelSerializer):

    player = serializers.StringRelatedField(
        required=False
    )
    game = serializers.StringRelatedField(
        required=False
    )

    class Meta:
        model = Bet
        fields = '__all__'