#!/usr/bin/env python3

# Quizzmaster discord bot for running digital pub quizzes through discord

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
import os
from datetime import timedelta
from flask import Flask, session
from flask_login import LoginManager, login_required
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Include modules
import config
import helpers.essentials as es
from modules.apiUser import apiUser
from modules.databaseInit import initDatabase


# Import data models to enable scheme creation
from models.user import User
from models.team import Team
from models.question import Question
from models.answer import Answer
from models.backendUser import BackendUser
from models.settings import Settings


# Include endpoints
from endpoints.scoreboard import scoreboardApi
from endpoints.guildjoin import guildJoinApi
from endpoints.login import loginApi
from endpoints.backenduser import backendUserApi
from endpoints.question import questionApi
from endpoints.team import teamApi
from endpoints.answer import answerApi
from endpoints.grading import gradingApi
from endpoints.settings import settingsApi


# First setup
if not os.path.exists(config.CONFIG_SECRET_KEY):
    with open(config.CONFIG_SECRET_KEY, "w") as f:
        f.write(es.randomString(40))


# Enable http (also in production because of https terminating proxy)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = 'true'


# Create server
quizzmaster = Flask(__name__)
SESSION_TYPE = "filesystem"
SESSION_COOKIE_NAME = "QUIZZMASTER_SESSION"
SESSION_COOKIE_SECURE = False  # Set this to true for production (SSL required)
SESSION_COOKIE_HTTPONLY = True
PERMANENT_SESSION_LIFETIME = 1200
quizzmaster.config.from_object(__name__)
with open(config.CONFIG_SECRET_KEY, "r") as f:
    quizzmaster.secret_key = f.read()
login_manager = LoginManager()
login_manager.init_app(quizzmaster)
login_manager.needs_refresh_message = (u"Session timed out, please re-login")
limiter = Limiter(
    quizzmaster,
    key_func=get_remote_address,
    default_limits=["10 per second"]
)


@login_manager.user_loader
def load_user(user_id):
    return apiUser(user_id)


# Set session timeout to 20 minutes
@quizzmaster.before_request
def before_request():
    session.permanent = True
    quizzmaster.permanent_session_lifetime = timedelta(minutes=20)


# Register blueprints
quizzmaster.register_blueprint(scoreboardApi)
quizzmaster.register_blueprint(guildJoinApi)
quizzmaster.register_blueprint(loginApi)
quizzmaster.register_blueprint(backendUserApi)
quizzmaster.register_blueprint(questionApi)
quizzmaster.register_blueprint(teamApi)
quizzmaster.register_blueprint(answerApi)
quizzmaster.register_blueprint(gradingApi)
quizzmaster.register_blueprint(settingsApi)


# EASTER EGG
@quizzmaster.route("/api/coffee", methods=["GET"])
def teapot():
    return "I'm a teapot", 418


# Init database
initDatabase()


# Create development server
if __name__ == "__main__":
    cors = CORS(quizzmaster, resources={r"/api/*": {"origins": "*"}})
    quizzmaster.run(debug=True, port=8081, threaded=True)
