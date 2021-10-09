#!/usr/bin/env python3

# OAuth functions

# Quizzmaster Discord bot for digital pub quizzes
# Copyright (C) 2021 Johannes Kreutz.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Include dependencies
from flask import session
from requests_oauthlib import OAuth2Session


# Include modules
import config


def tokenUpdater(token):
    session['oauth2_token'] = token


def makeSession(token=None, state=None, scope=None):
    return OAuth2Session(
        client_id=config.CONFIG_OAUTH2_CLIENT_ID,
        token=token,
        state=state,
        scope=scope,
        redirect_uri=config.CONFIG_BASE_DOMAIN + "/api/join/callback",
        auto_refresh_kwargs={
            'client_id': config.CONFIG_OAUTH2_CLIENT_ID,
            'client_secret': config.CONFIG_OAUTH2_CLIENT_SECRET,
        },
        auto_refresh_url=config.CONFIG_DISCORD_API_BASE + "/oauth2/token",
        token_updater=tokenUpdater)
