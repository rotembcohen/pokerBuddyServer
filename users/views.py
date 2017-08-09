# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from users.models import User
from users.serializers import UserSerializer
from games.models import Bet
from games.serializers import BetSerializer


class UserViewSet(viewsets.ModelViewSet):
	queryset = User.objects.all()
	serializer_class = UserSerializer

	#TODO: change permissions to user only?
	@detail_route(methods=['get'], permission_classes=[IsAuthenticated])
	def active_games(self,request,pk=None):

		active_bets = Bet.objects.filter(game__is_active=True,player__pk=pk)

		serializer = BetSerializer(
			active_bets,
			many=True,
			context={'request': request}
		)

		return Response(serializer.data)