# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from users.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Game(models.Model):
	identifier = models.CharField(max_length=10)
	min_bet = models.PositiveIntegerField(default=20)
	players = models.ManyToManyField(User,related_name='players')
	host = models.ForeignKey(User, on_delete=models.CASCADE,related_name='host')
	is_active = models.BooleanField(default=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.identifier
    	

