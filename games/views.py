# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from games.models import Game, Bet
from games.serializers import GameSerializer, BetSerializer
from rest_framework.decorators import detail_route

import random
import string

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
    	#randomize identifier
    	IDENTIFIER_LEN = 5
        identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(IDENTIFIER_LEN))

        #associate host to current logged in user
        host = self.request.user

        #create active game
        is_active = True
    	
    	serializer.save(host=host,identifier=identifier,is_active=is_active)

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self,serializer):
		#TODO:allow for different player to be specified
		player = self.request.user

		#get game
		game = get_object_or_404(Game,identifier=self.request.POST['game_identifier'],is_active=True)

		serializer.save(player=player, game=game)





		

    