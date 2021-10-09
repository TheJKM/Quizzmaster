#!/usr/bin/env python3

# Settings API

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
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import exc


# Include modules
from models.settings import Settings
from models.team import Team
from modules.database import database
import config


# Endpoint definition
settingsApi = Blueprint("settingsApi", __name__)


@settingsApi.route("/api/teamregistration", methods=["GET"])
def teamRegistrationOpen():
    dbSession = database.createSession()
    enabled = dbSession.query(Settings).filter(Settings.key == "teamRegistrationOpen").first()
    if enabled.value == "false":
        dbSession.close()
        return "CLOSED", 200
    teams = dbSession.query(Team).all()
    if len(teams) >= config.CONFIG_MAX_TEAM_COUNT:
        dbSession.close()
        return "FULL", 200
    dbSession.close()
    return "OPEN", 200


@settingsApi.route("/api/setting", methods=["GET"])
@login_required
def getSetting():
    dbSession = database.createSession()
    setting = dbSession.query(Settings).all()
    response = []
    for s in setting:
        response.append({
            "key": s.key,
            "value": s.value
        })
    dbSession.close()
    return jsonify(response), 200


@settingsApi.route("/api/setting/<key>/<value>", methods=["POST"])
@login_required
def setSetting(key, value):
    dbSession = database.createSession()
    setting = dbSession.query(Settings).filter(Settings.key == key).first()
    setting.value = value
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    return "SUCCESS", 200
