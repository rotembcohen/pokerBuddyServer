# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from games.models import Game, Bet
from games.serializers import GameSerializer

#from pokerBuddyServer import notifications

import pusher
import random
import string

pusher_client = pusher.Pusher(
	app_id='382853',
	key='442e9fce1c86b001266e',
	secret='c8da83b9b8390ec9a2c3',
	cluster='us2',
	ssl=True
)

class GameViewSet(viewsets.ModelViewSet):
	queryset = Game.objects.all()
	serializer_class = GameSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
	lookup_field = 'identifier'

	def perform_create(self, serializer):
		#randomize identifier
		IDENTIFIER_LEN = 5
		identifier = ''.join(random.choice(string.ascii_uppercase) for _ in range(IDENTIFIER_LEN))

		#associate host to current logged in user
		host = self.request.user

		#create active game
		is_active = True

		serializer.save(host=host,identifier=identifier,is_active=is_active)


	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def join_game(self,request,identifier=None):

		#TODO: check if user already in the game
		if request.data['player_id']:
			player = get_object_or_404(User,pk=request.data['player_id'])
		else:
			player = request.user

		game = Game.objects.get(identifier=identifier)

		bet, created = Bet.objects.get_or_create(
			game=game,
			player=player,
		)

		if created:
			#created, set bet to game's bet
			#TODO: allow for special cases?
			bet.amount = game.min_bet
			bet.save()
		
			
			#TODO: this is an example of how it works. this should be used in the payView when ready
			#send push notifications:
			# for b in bet.game.bets.exclude(player__push_token__isnull=True)
			# 	notifications.send_push_message(b.player.push_token, str(player) + " joined your game",{game_identifier:identifier})
		
		serializer = GameSerializer(context={'request': request},instance=game)

		pusher_client.trigger(bet.game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	#TODO: change permissions to user only? may contradict "allow different player"
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def buy_in(self,request,identifier=None):

		if request.data['player_id']:
			player = get_object_or_404(User,pk=request.data['player_id'])
		else:
			player = request.user
		
		#TODO:duplicate code?
		#TODO:get_or_404
		
		bet = Bet.objects.get(player=player,game__identifier=identifier,game__is_active=True)

		#update amount and clear result
		bet.amount = bet.amount + request.data['amount']
		bet.result = None

		bet.save()

		serializer = GameSerializer(context={'request': request},instance=bet.game)

		pusher_client.trigger(bet.game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	#TODO: change permissions to user only? may contradict "allow different player"
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def leave_game(self,request,identifier=None):

		if request.data['player_id']:
			player = get_object_or_404(User,pk=request.data['player_id'])
		else:
			player = request.user

		bet = Bet.objects.get(player=player,game__identifier=identifier)

		bet.result = request.data['result']
		bet.save()

		serializer = GameSerializer(context={'request': request}, instance=bet.game)

		pusher_client.trigger(bet.game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	#TODO: change permissions to host only
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def finish_game(self,request,identifier=None):

		game = get_object_or_404(Game,identifier=identifier);
		game.is_active = False;
		game.save()

		serializer = GameSerializer(context={'request': request}, instance=game)

		return Response(serializer.data)

