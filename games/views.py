# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.shortcuts import get_object_or_404
from rest_framework import viewsets, permissions
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from games.models import Game, Bet, Payment
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

		pusher_client.trigger(game.identifier, 'game-update', {'game': serializer.data});

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

		#TODO: make sure all bet results sum to 0 before finishing game

		game = get_object_or_404(Game,identifier=identifier)
		game.is_active = False
		game.save()

		sorted_bets = sorted(game.bets.all(),key=lambda t: t.amount - t.result)
		i = 0
		j = len(sorted_bets)-1
		loss_leftovers = 0
		
		while i < len(sorted_bets):
			
			#break if current i is loser
			current_win = sorted_bets[i].result - sorted_bets[i].amount
			if current_win <= 0:
				break
			
			amount_left_in_bet = current_win

			while amount_left_in_bet > 0:

				p = Payment()
				p.is_confirmed = False
				p.bet = sorted_bets[i]
				p.source = sorted_bets[j].player

				#how much does loser needs to pay?
				if loss_leftovers > 0:
					current_loss = loss_leftovers
				else:
					#break if current j is winner
					current_loss = -1 * (sorted_bets[j].result - sorted_bets[j].amount)
					if current_loss <= 0:
						break
				
				#how much winner needs to receive?
				if amount_left_in_bet >= current_loss:
					#current winner needs more or equal to what loser lost
					p.amount = current_loss
					p.save()
					
					#continue to next loser with updated amount
					amount_left_in_bet = amount_left_in_bet - current_loss
					loss_leftovers = 0
					j = j - 1
				
				else:
					#current winner needs less than loser lost
					p.amount = amount_left_in_bet
					p.save()
					
					loss_leftovers = current_loss - amount_left_in_bet
					amount_left_in_bet = 0
			#end while
			i = i + 1
		#end while					

		serializer = GameSerializer(context={'request': request}, instance=game)

		pusher_client.trigger(game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)


	#TODO: permissions to host and player only
	#TODO: change identifier to payment_id
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def confirm_payment_receipt(self,request,identifier=None):

		payment_id = request.data['payment_id']
		
		payment = get_object_or_404(Payment,pk=payment_id)
		payment.is_confirmed = True
		payment.save()

		game = payment.bet.game
		
		serializer = GameSerializer(context={'request': request}, instance=game)

		pusher_client.trigger(game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	#TODO: change permissions to user and host only
	#TODO: remove this when 0.2 is retired
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def confirm_payment(self,request,identifier=None):

		source = get_object_or_404(User,pk=request.data['source_id'])
		amount = request.data['amount']
		target = get_object_or_404(User,pk=request.data['target_id'])

		if source == target:
			#TODO:should be error
			return

		#TODO: also check if amount bigger than result amount

		bet = get_object_or_404(Bet,game__identifier=identifier,player=target)

		payment, created = Payment.objects.get_or_create(
			source=source,
			bet=bet,
			defaults={'amount':amount}
		)

		#overrides amount if not equal
		if not created:
			payment.amount = amount
			payment.save()
		
		serializer = GameSerializer(context={'request': request}, instance=bet.game)

		pusher_client.trigger(bet.game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	#TODO: change permissions to game host only
	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def approve_game(self,request,identifier=None):

		game = get_object_or_404(Game,identifier=identifier)
		is_approved = request.data['is_approved']

		#make sure input val is boolean
		if not isinstance(is_approved, bool):
			#TODO: should be error
			return

		game.is_approved = is_approved
		game.save()

		serializer = GameSerializer(context={'request': request}, instance=game)

		pusher_client.trigger(game.identifier, 'game-update', {'game': serializer.data});

		return Response(serializer.data)

	@list_route()
	def active_games(self, request):
		user = request.user
		q = self.get_queryset().filter(bets__player=user,is_active=True).values('identifier')
		return Response(list(q))

	@list_route()
	def past_games(self, request):
		user = request.user
		q = self.get_queryset().filter(bets__player=user,is_active=False).values('identifier')
		return Response(list(q))
