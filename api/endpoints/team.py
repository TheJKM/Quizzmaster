#!/usr/bin/env python3

# Team API

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
from flask import Blueprint, jsonify
from flask_login import login_required, current_user
import json


# Include modules
from models.team import Team
from models.user import User
from modules.database import database
from modules.permission import permission
import config


# Endpoint definition
teamApi = Blueprint("teamApi", __name__)


@teamApi.route("/api/team", methods=["GET"])
@login_required
def getTeams():
    if not permission.checkAdmin(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    teams = dbSession.query(Team).all()
    response = {
        "teams": [],
        "teamInformation": [],
    }
    first = True
    for t in teams:
        if first:
            first = False
            for question in config.CONFIG_REGISTER_QUESTIONS:
                response["teamInformation"].append(question["question"])
        memberQuery = dbSession.query(Team, User).filter(Team.id == t.id).filter(User.teamId == Team.id)
        memberCount = memberQuery.count()
        captain = dbSession.query(User).filter(User.isCaptain == True).filter(User.teamId == t.id).first()
        response["teams"].append({
            "id": t.id,
            "name": t.name,
            "information": json.loads(t.information),
            "memberCount": memberCount,
            "captainEmail": captain.email if captain is not None else "-",
            "displayId": t.displayId,
        })
        if captain is not None:
            if not captain.registrationStatus == "added":
                response["teams"][-1]["regisrationSuccess"] = False
                response["teams"][-1]["finalizeLink"] = config.CONFIG_BASE_DOMAIN + "/api/join/authenticate/" + str(captain.id) + "/" + str(t.id)
            else:
                response["teams"][-1]["regisrationSuccess"] = True
    dbSession.close()
    return jsonify(response), 200
