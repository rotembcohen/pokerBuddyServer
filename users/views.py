# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from games.models import Bet
from games.serializers import BetSerializer


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer
	
	def get_permissions(self):
		# allow non-authenticated user to create via POST
		return (AllowAny() if self.request.method == 'POST'
			else IsAuthenticated()),

	#TODO: change permissions to user only?
	#TODO: also protect info change by non target user
	@detail_route(methods=['get'], permission_classes=[IsAuthenticated])
	def active_games(self,request,pk=None):

		active_bets = Bet.objects.filter(game__is_active=True,player__pk=pk)

		serializer = BetSerializer(
			active_bets,
			many=True,
			context={'request': request}
		)

		return Response(serializer.data)

	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def update_venmo(self,request,pk=None):

		user = get_object_or_404(User,pk=pk)
		user.venmo_username = request.data['venmo_username']
		user.save()

		serializer = UserSerializer(context={'request': request}, instance=user)

		return Response(serializer.data)

	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def push_token(self,request,pk=None):

		user = get_object_or_404(User,pk=pk)
		user.push_token = request.data['push_token']
		user.save()
		
		serializer = UserSerializer(context={'request': request}, instance=user)

		return Response(serializer.data)
