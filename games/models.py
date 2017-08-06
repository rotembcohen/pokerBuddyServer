# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import random
import string

from django.db import models

from users.models import User

class Game(models.Model):
	IDENTIFIER_LEN = 5

	identifier = models.CharField(max_length=10)
	min_bet = models.PositiveIntegerField(default=20)
	players = models.ManyToManyField(User,related_name='players')
	host = models.ForeignKey(User, on_delete=models.CASCADE,related_name='host')
	is_active = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __init__(self):
		super(Game,self).__init__()
		self.identifier = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(IDENTIFIER_LEN))

	def __unicode__(self):
		return self.identifier

