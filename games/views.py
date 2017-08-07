# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from games.models import Game, Bet
from games.serializers import GameSerializer

import random
import string

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    lookup_field = 'identifier'

    def perform_create(self, serializer):
    	#randomize identifier
    	IDENTIFIER_LEN = 5
        identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(IDENTIFIER_LEN))

        #associate host to current logged in user
        host = self.request.user

        #create active game
        is_active = True
    	
    	serializer.save(host=host,identifier=identifier,is_active=is_active)


    @detail_route(methods=['post'], permission_classes=[IsAuthenticated])
    def join_game(self,request,identifier=None):
	    
    	#TODO:allow for different player to be specified
		player = request.user

		game = Game.objects.get(identifier=identifier)

		bet, created = Bet.objects.get_or_create(
			game=game,
			player=player
		)

		serializer = GameSerializer(context={'request': request},instance=game)

		return Response(serializer.data)

		
	




		

    