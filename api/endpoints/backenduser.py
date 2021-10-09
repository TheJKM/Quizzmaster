#!/usr/bin/env python3

# Backend user API

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
from flask_login import current_user, login_required
from passlib.hash import bcrypt
from sqlalchemy import exc


# Include modules
from models.backendUser import BackendUser
from modules.database import database
from modules.permission import permission


# Endpoint definition
backendUserApi = Blueprint("backendUserApi", __name__)


@backendUserApi.route("/api/backenduser", methods=["GET", "PUT"])
@login_required
def createUser():
    if not permission.checkAdmin(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    if request.method == "GET":
        backenduser = dbSession.query(BackendUser).all()
        ids = []
        for b in backenduser:
            ids.append({
                "id": b.id,
                "username": b.username,
                "isAdmin": b.isAdmin,
                "isQuestionmaker": b.isQuestionmaker,
                "isGrading": b.isGrading
            })
        dbSession.close()
        return jsonify(ids), 200
    elif request.method == "PUT":
        grading = True if request.form.get("grading") == "true" else False
        questionmaker = True if request.form.get("questionmaker") == "true" else False
        admin = True if request.form.get("admin") == "true" else False
        newUser = BackendUser(request.form.get("username"), bcrypt.hash(request.form.get("password")), grading, questionmaker, admin)
        dbSession.add(newUser)
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        return "SUCCESS", 201


@backendUserApi.route("/api/backenduser/<id>", methods=["DELETE", "POST"])
@login_required
def deleteUser(id):
    if not permission.checkAdmin(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    user = dbSession.query(BackendUser).filter(BackendUser.id == id).first()
    if request.method == "DELETE":
        dbSession.delete(user)
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        return "SUCCESS", 200
    elif request.method == "POST":
        if "isAdmin" in request.form.keys():
            user.isAdmin = True if request.form.get("isAdmin") == "true" else False
        elif "isQuestionmaker" in request.form.keys():
            user.isQuestionmaker = True if request.form.get("isQuestionmaker") == "true" else False
        elif "isGrading" in request.form.keys():
            user.isGrading = True if request.form.get("isGrading") == "true" else False
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        return "SUCCESS", 200
