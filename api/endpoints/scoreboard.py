#!/usr/bin/env python3

# Scoreboard API

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
from flask_login import login_required
from sqlalchemy import func


# Include modules
from models.team import Team
from models.answer import Answer
from models.question import Question
from modules.database import database
from enums.questionState import questionState


# Endpoint definition
scoreboardApi = Blueprint("scoreboardApi", __name__)


@scoreboardApi.route("/api/scoreboard", methods=["GET"])
def publicScoreboard():
    dbSession = database.createSession()
    teams = dbSession.query(Team.name, Team.displayId, func.sum(Answer.points).label("points")).join(Answer).join(Question).filter(Question.state == questionState.published).group_by(Team.id).all()
    result = {
        "teams": [],
        "questions": []
    }
    sortedTeams = sorted(teams, key=lambda t: t["points"], reverse=True)
    for team in sortedTeams:
        p = 0 if team.points is None else team.points
        result["teams"].append({
            "name": team.name,
            "displayId": team.displayId,
            "points": p,
        })
    questions = dbSession.query(Question.displayId).filter(Question.state == questionState.published).order_by(Question.displayId).all()
    for question in questions:
        result["questions"].append(question.displayId)
    dbSession.close()
    return jsonify(result), 200


@scoreboardApi.route("/api/scoreboard-private", methods=["GET"])
@login_required
def privateScoreboard():
    dbSession = database.createSession()
    result = {
        "questions": [],
        "teams": []
    }
    teams = dbSession.query(Team).all()
    for team in teams:
        t = {
            "answers": [],
            "name": str(team.displayId) + " (" + team.name + ")",
            "id": team.id
        }
        result["teams"].append(t)
    dbSession.close()
    dbSession = database.createSession()
    for team in result["teams"]:
        answers = dbSession.query(Answer).filter(Answer.teamId == team["id"]).all()
        for answer in answers:
            a = {
                "questionId": answer.questionId,
                "points": answer.points,
                "id": answer.id,
                "questionId": answer.questionId
            }
            team["answers"].append(a)
    dbSession.close()
    dbSession = database.createSession()
    questions = dbSession.query(Question).order_by(Question.displayId).all()
    for question in questions:
        result["questions"].append({
            "displayId": question.displayId,
            "state": question.state.value,
            "id": question.id,
            "question": question.title,
            "hint": question.gradingHint,
            "maxPoints": question.maxPoints,
            "type": question.type.value,
            "options": question.options
        })
    dbSession.close()
    return jsonify(result), 200
