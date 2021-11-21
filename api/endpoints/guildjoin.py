#!/usr/bin/env python3

# Guild join API

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
from flask import Blueprint, request, redirect, session, jsonify
from sqlalchemy import exc
import requests
import json
import re


# Include modules
from models.settings import Settings
from models.team import Team
from models.user import User
from enums.registrationState import registrationState
from modules.database import database
from modules.teamid import teamid
from modules.discordDispatcher import discordDispatcher
from modules.mail import mail
import modules.oauth as oauth
import config


# Endpoint definition
guildJoinApi = Blueprint("guildJoinApi", __name__)


@guildJoinApi.route("/api/join/questions", methods=["GET"])
def guildJoinQuestions():
    return jsonify({
        "questions": config.CONFIG_REGISTER_QUESTIONS,
        "welcomeText": config.CONFIG_LANDING_PAGE_TEXT,
        "welcomeTitle": config.CONFIG_LANDING_PAGE_TITLE,
        "consentText": config.CONFIG_SIGNUP_CONSENT,
        "discordExplanation": config.CONFIG_DISCORD_EXPLANATION,
    })


@guildJoinApi.route("/api/join/checkid/<id>", methods=["GET"])
def guildJoinCheckTeamId(id):
    dbSession = database.createSession()
    team = dbSession.query(Team).filter(Team.displayId == id).first()
    if team is None:
        dbSession.close()
        return "UNKNOWN", 200
    else:
        dbSession.close()
        return "EXISTS", 200


@guildJoinApi.route("/api/join/start", methods=["PUT"])
def guildJoinStart():
    dbSession = database.createSession()
    if request.form.get("isNewTeam") == "true":
        enabled = dbSession.query(Settings).filter(Settings.key == "teamRegistrationOpen").first()
        if enabled.value == "false":
            dbSession.close()
            return "ERR_CLOSED", 500
        teams = dbSession.query(Team).filter(Team.displayId.isnot(None)).all()
        if len(teams) >= config.CONFIG_MAX_TEAM_COUNT:
            dbSession.close()
            return "ERR_CLOSED", 500
        if request.form.get("teamName") == "":
            return "ERR_TEAMNAME", 406
        regex = re.compile('^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$')
        if not regex.search(request.form.get("email")):
            return "ERR_EMAIL", 406
        team = Team(request.form.get("teamName"), request.form.get("teamInformation"))
        dbSession.add(team)
        user = User(True, email=request.form.get("email"))
    else:
        team = dbSession.query(Team).filter(Team.displayId == request.form.get("teamId")).first()
        if team is None:
            dbSession.close()
            return "ERR_INVALID_TEAM_ID", 500
        user = User(False, teamId=team.id)
    dbSession.add(user)
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    response = {
        "user": str(user.id),
        "team": str(team.id),
    }
    dbSession.close()
    return jsonify(response), 200


@guildJoinApi.route("/api/join/authenticate/<id>/<team>", methods=["GET"])
def guildJoinAuthenticate(id, team):
    scope = ["guilds.join", "identify"]
    discord = oauth.makeSession(scope=scope)
    authorizationUrl, state = discord.authorization_url(config.CONFIG_DISCORD_API_BASE + "/oauth2/authorize")
    session["oauth2_state"] = state
    session["database_user_id"] = id
    session["database_team_id"] = team
    return redirect(authorizationUrl)


@guildJoinApi.route("/api/join/callback", methods=["GET"])
def guildJoinCallback():
    if request.values.get("error"):
        return request.values["error"]
    discord = oauth.makeSession(state=session.get("oauth2_state"))
    token = discord.fetch_token(
        config.CONFIG_DISCORD_API_BASE + "/oauth2/token",
        client_secret=config.CONFIG_OAUTH2_CLIENT_SECRET,
        authorization_response=request.url)
    session["oauth2_token"] = token
    userData = json.loads(discord.get(config.CONFIG_DISCORD_API_BASE + "/users/@me").text)
    session["discord_user_id"] = userData["id"]
    return redirect("/api/join/finalize")


@guildJoinApi.route("/api/join/finalize", methods=["PUT", "GET"])
def guildJoinFinalize():
    url = config.CONFIG_DISCORD_API_BASE + "/guilds/" + config.CONFIG_DISCORD_SERVER + "/members/" + session["discord_user_id"]
    headers = {
        "Authorization": "Bot " + config.CONFIG_BOT_TOKEN,
        "Content-Type": "application/json"
    }
    data = {
        "access_token": session["oauth2_token"]["access_token"]
    }
    response = requests.put(url=url, json=data, headers=headers)
    if response.status_code == 201:
        dbSession = database.createSession()
        user = dbSession.query(User).filter(User.id == session["database_user_id"]).first()
        if user is None:
            dbSession.close()
            return redirect(config.CONFIG_BASE_DOMAIN + "/start_session")
        user.teamId = session["database_team_id"]
        user.discordId = session["discord_user_id"]
        user.registrationStatus = registrationState.added
        team = dbSession.query(Team).filter(Team.id == session["database_team_id"]).first()
        if team is None:
            dbSession.close()
            return redirect(config.CONFIG_BASE_DOMAIN + "/start_session")
        if user.isCaptain:
            team.displayId = teamid.generate(session["database_team_id"])
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return redirect(config.CONFIG_BASE_DOMAIN + "/start_database")
        discord = discordDispatcher()
        discord.createChannel(team.displayId, user.isCaptain, session["discord_user_id"], team.name)
        del discord
        if user.isCaptain:
            url = config.CONFIG_BASE_DOMAIN + "/" + team.displayId
            if mail.send(team.name, team.displayId, url, user.email) < 0:
                dbSession.close()
                return redirect(config.CONFIG_BASE_DOMAIN + "/start_mail")
        dbSession.close()
        return redirect(config.CONFIG_BASE_DOMAIN + "/start_success")
    else:
        return redirect(config.CONFIG_BASE_DOMAIN + "/start_discord")
