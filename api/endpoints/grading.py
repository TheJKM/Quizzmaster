#!/usr/bin/env python3

# Grading API

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
from models.answer import Answer
from models.question import Question
from modules.database import database
from modules.permission import permission
from enums.questionState import questionState
from enums.questionType import questionType


# Endpoint definition
gradingApi = Blueprint("gradingApi", __name__)


@gradingApi.route("/api/grading/available", methods=["GET"])
@login_required
def gradingAvailable():
    if not permission.checkGrading(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    questions = dbSession.query(Question).filter(Question.state == questionState.inGrading).filter(Question.type == questionType.text).all()
    for question in questions:
        answers = dbSession.query(Answer).filter(Answer.questionId == question.id).filter(Answer.graderAssigned == None).count()
        if answers > 0:
            dbSession.close()
            return "SUCCESS", 200
    dbSession.close()
    return "EMPTY", 200


@gradingApi.route("/api/grading/apply", methods=["POST"])
@login_required
def applyForGrading():
    if not permission.checkGrading(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    questions = dbSession.query(Question).filter(Question.state == questionState.inGrading).filter(Question.type == questionType.text).all()
    for question in questions:
        answer = dbSession.query(Answer).filter(Answer.questionId == question.id).filter(Answer.graderAssigned == None).first()
        if answer is not None:
            answer.graderAssigned = True
            result = {
                "id": answer.id,
                "value": answer.value,
                "question": question.title,
                "category": question.category,
                "hint": question.gradingHint,
                "maxPoints": question.maxPoints
            }
            try:
                dbSession.commit()
                dbSession.close()
            except exc.SQLAlchemyError:
                dbSession.close()
            return jsonify(result), 200
    dbSession.close()
    return "EMPTY", 200


@gradingApi.route("/api/grading/<id>", methods=["POST"])
@login_required
def gradeAnswer(id):
    if not permission.checkGrading(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    answer = dbSession.query(Answer).filter(Answer.id == id).first()
    answer.points = float(request.form.get("points"))
    openAnswers = dbSession.query(Answer).filter(Answer.questionId == answer.questionId).filter(Answer.points == None).count()
    if openAnswers == 0:
        question = dbSession.query(Question).filter(Question.id == answer.questionId).first()
        question.state = questionState.waitForPublishing
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200
