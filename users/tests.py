# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory, Client
from django.urls import reverse
from users.models import User
from pokerBuddyServer.views import CustomObtainAuthToken

import json

# Create your tests here.
class UsersModelTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create_user(username='testplayer',password='top_secret')

	def test_users_were_created(self):

		count = User.objects.all().count()
		self.assertIs(count,1)

	def test_was_authenticated(self):

		request = self.factory.post(reverse('auth'),
									{
										'username': self.user.username,
										'password': 'top_secret'
									})
		response = CustomObtainAuthToken.as_view()(request)
		objectResponse = json.loads(response.rendered_content)
		
		self.assertEquals(self.user.id,objectResponse['user']['id'])