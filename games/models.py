# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from decimal import *

from users.models import User
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.core.validators import MinValueValidator

class Game(models.Model):
	#TODO: should be unique
	identifier = models.CharField(max_length=10)
	min_bet = models.DecimalField(default=20.0,max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
	host = models.ForeignKey(User, on_delete=models.CASCADE,related_name='host')
	is_active = models.BooleanField(default=True)
	is_approved = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.identifier
    	
class Bet(models.Model):
	player = models.ForeignKey(User,related_name='bets',on_delete=models.CASCADE)
	game = models.ForeignKey(Game,related_name='bets',on_delete=models.CASCADE)
	amount = models.DecimalField(default=20.0,max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
	result = models.DecimalField(default=None,max_digits=12,null=True,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.player) + ": " + str(self.amount)

class Payment(models.Model):
	bet = models.ForeignKey(Bet,related_name='payments',on_delete=models.CASCADE)
	source = models.ForeignKey(User,related_name='payments',on_delete=models.CASCADE)
	amount = models.DecimalField(default=0.0,max_digits=12,decimal_places=2,validators=[MinValueValidator(Decimal('0.01'))])
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return str(self.amount) + " of " + str(self.bet) + " paid by " + str(self.source)
