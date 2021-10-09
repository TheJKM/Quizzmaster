#!/usr/bin/env python3

# Answer API

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


# Include modules
from models.answer import Answer
from modules.database import database
from modules.permission import permission


# Endpoint definition
answerApi = Blueprint("answerApi", __name__)


@answerApi.route("/api/answer/<id>", methods=["GET", "POST"])
@login_required
def answer(id):
    if not permission.checkAdmin(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    if request.method == "GET":
        answer = dbSession.query(Answer).filter(Answer.id == id).first()
        response = {
            "value": answer.value,
            "points": answer.points,
        }
        dbSession.close()
        return jsonify(response), 200
    elif request.method == "POST":
        answer = dbSession.query(Answer).filter(Answer.id == id).first()
        answer.points = float(request.form.get("points"))
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        return "SUCCESS", 200
