#!/usr/bin/env python3

# Login API

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
from flask_login import login_user, logout_user, current_user, login_required
from passlib.hash import bcrypt


# Include modules
from models.backendUser import BackendUser
from modules.apiUser import apiUser
from modules.database import database


# Endpoint definition
loginApi = Blueprint("loginApi", __name__)


@loginApi.route("/api/login", methods=["POST"])
def login():
    if not "username" in request.form.keys() or not "password" in request.form.keys():
        return "DATA_MISSING", 400
    dbSession = database.createSession()
    user = dbSession.query(BackendUser).filter(BackendUser.username == request.form.get("username")).first()
    if user is None:
        dbSession.close()
        return "ERR_WRONG_DATA", 403
    try:
        if bcrypt.verify(request.form.get("password"), user.password):
            loggedInAccount = apiUser(user.id)
            login_user(loggedInAccount)
            dbSession.close()
            return "SUCCESS", 200
        else:
            dbSession.close()
            return "ERR_WRONG_DATA", 403
    except ValueError:
        return "ERR_INTERNAL", 500


@loginApi.route("/api/logout", methods=["POST"])
def logout():
    logout_user()
    return "SUCCESS", 200


@loginApi.route("/api/permission", methods=["GET"])
@login_required
def permission():
    dbSession = database.createSession()
    user = dbSession.query(BackendUser).filter(BackendUser.username == current_user.username).first()
    permissions = {
        "isAdmin": user.isAdmin,
        "isGrading": user.isGrading,
        "isQuestionmaker": user.isQuestionmaker
    }
    dbSession.close()
    return jsonify(permissions), 200
