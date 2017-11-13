# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase, RequestFactory, Client

from users.models import User

# Create your tests here.
class UsersModelTest(TestCase):

	def setUp(self):
		self.factory = RequestFactory()
		self.user = User.objects.create(username='testplayer',password='top_secret')

	def test_was_authenticated(self):

		count = User.objects.all().count()
		self.assertIs(count,1)

		self.assertEqual(self.user.username,u'testplayer')
