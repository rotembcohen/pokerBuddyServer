# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from rest_framework import routers, serializers, viewsets, status, permissions
from rest_framework.decorators import detail_route, list_route, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from users.models import User
from users.serializers import UserSerializer, ChangePasswordSerializer
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

		active_bets = Bet.objects.filter(game__is_active=True,player__pk=pk).order_by('-created_at')

		serializer = BetSerializer(
			active_bets,
			many=True,
			context={'request': request}
		)

		return Response(serializer.data)

	#TODO: change permissions to user only?
	#TODO: also protect info change by non target user
	@detail_route(methods=['get'], permission_classes=[IsAuthenticated])
	def past_games(self,request,pk=None):

		past_bets = Bet.objects.filter(game__is_active=False,player__pk=pk).order_by('-created_at')

		serializer = BetSerializer(
			past_bets,
			many=True,
			context={'request': request}
		)

		return Response(serializer.data)

	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def update_settings(self,request,pk=None):

		user = get_object_or_404(User,pk=pk)
		user.venmo_username = request.data['venmo_username']
		user.default_min_bet = request.data['default_min_bet']
		user.buy_in_intervals = request.data['buy_in_intervals']
		user.chip_basic_unit = request.data['chip_basic_unit']
		user.save()

		serializer = UserSerializer(context={'request': request}, instance=user)

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

	@detail_route(methods=['post'], permission_classes=[IsAuthenticated])
	def update_app_version(self,request,pk=None):
	
		user = get_object_or_404(User,pk=pk)
		user.app_version = request.data['app_version']
		user.save()

		serializer = UserSerializer(context={'request': request}, instance=user)

		return Response(serializer.data)

class UpdatePassword(APIView):
    """
    An endpoint for changing password.
    """
    permission_classes = (permissions.IsAuthenticated, )

    def get_object(self, queryset=None):
        return self.request.user

    def put(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = ChangePasswordSerializer(data=request.data)

        if serializer.is_valid():
            # Check old password
            old_password = serializer.data.get("old_password")
            if not self.object.check_password(old_password):
                return Response({"old_password": ["Wrong password."]}, 
                                status=status.HTTP_400_BAD_REQUEST)
            # set_password also hashes the password that the user will get
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response(status=status.HTTP_204_NO_CONTENT)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

