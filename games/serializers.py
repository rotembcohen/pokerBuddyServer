from rest_framework import serializers
from games.models import Game
from users.models import User

class GameSerializer(serializers.HyperlinkedModelSerializer):
    
    identifier = serializers.CharField(required=False,read_only=True)
    players = serializers.HyperlinkedRelatedField(
        queryset=User.objects.all(),required=False,many=True,view_name='user-detail'
    )
    host = serializers.StringRelatedField(
        required=False
    )

    class Meta:
        model = Game
        fields = '__all__'