from rest_framework import serializers
from games.models import Game


class GameSerializer(serializers.HyperlinkedModelSerializer):
    token = serializers.CharField(read_only=True)

    class Meta:
        model = Game
        fields = '__all__'