# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from games.models import Game, Bet

admin.site.register(Game)
admin.site.register(Bet)
