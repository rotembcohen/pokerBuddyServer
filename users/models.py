# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

class User(AbstractUser):
	venmo_username = models.CharField(max_length=255, blank=True, null=True)
	phone_number = models.CharField(max_length=255, blank=True, null=True)
	facebook_token = models.CharField(max_length=255, blank=True, null=True)
	picture_url = models.CharField(max_length=255, blank=True, null=True)
	push_token = models.CharField(max_length=255, blank=True, null=True)

	def __unicode__(self):
		if (self.first_name and self.last_name):
			return self.first_name + " " + self.last_name
		else:
			return self.username

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)