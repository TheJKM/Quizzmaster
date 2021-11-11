#!/usr/bin/env python3

# Question API

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
from flask import Blueprint, request, jsonify, Response
from flask_login import login_required, current_user
from sqlalchemy import exc
import json
import datetime


# Include modules
from models.question import Question
from models.answer import Answer
from modules.database import database
from modules.permission import permission
from modules.discordDispatcher import discordDispatcher
from modules.automaticGrading import autoGrade
from enums.questionType import questionType
from enums.questionState import questionState
from helpers.fixQuestionIds import fixQuestionIds
from customGrading.manager import CustomGradingManager


# Endpoint definition
questionApi = Blueprint("questionApi", __name__)


@questionApi.route("/api/question", methods=["GET", "PUT"])
@login_required
def getQuestions():
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    if request.method == "GET":
        questions = dbSession.query(Question).order_by(Question.displayId).all()
        ids = []
        for q in questions:
            ids.append({
                "id": q.id,
                "displayId": q.displayId,
                "question": q.title,
                "category": q.category,
                "type": q.type.value,
                "state": q.state.value
            })
        dbSession.close()
        return jsonify(ids), 200
    elif request.method == "PUT":
        if request.form.get("type") == "multipleChoice":
            type = questionType.multipleChoice
        elif request.form.get("type") == "trueFalse":
            type = questionType.trueFalse
        elif request.form.get("type") == "customAutomatic":
            type = questionType.custom
        elif request.form.get("type") == "customManual":
            type = questionType.external
        elif request.form.get("type") == "customMc":
            type = questionType.customMc
        else:
            type = questionType.text
        questions = dbSession.query(Question).order_by(Question.displayId).all()
        if len(questions) <= 0:
            newId = 1
        else:
            newId = questions[-1].displayId + 1
        maxPoints = float(request.form.get("maxPoints"))
        question = Question(request.form.get("title"), request.form.get("category"), type, newId, maxPoints)
        question.gradingHint = request.form.get("hint")
        if request.form.get("type") == "multipleChoice" or request.form.get("type") == "customMc":
            question.options = request.form.get("options")
            if request.form.get("type") == "multipleChoice":
                question.correctAnswer = request.form.get("correctAnswer")
        elif request.form.get("type") == "trueFalse":
            question.correctAnswer = request.form.get("correctAnswer")
        if request.form.get("type") == "customAutomatic" or request.form.get("type") == "customMc":
            question.customGradingFunction = request.form.get("customFunction")
        dbSession.add(question)
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        if not fixQuestionIds(dbSession):
            return "ERR_DATABASE", 500
        return "SUCCESS", 200

@questionApi.route("/api/question/<id>", methods=["GET", "POST", "DELETE"])
@login_required
def getQuestion(id):
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    if request.method == "GET":
        question = dbSession.query(Question).filter(Question.id == id).first()
        if question is None:
            dbSession.close()
            return "ERR_NOT_FOUND", 404
        dbSession.close()
        return jsonify({
            "options": question.options,
            "gradingHint": question.gradingHint,
            "correctAnswer": question.correctAnswer,
            "maxPoints": question.maxPoints,
        }), 200
    elif request.method == "POST":
        question = dbSession.query(Question).filter(Question.id == id).first()
        if question is None:
            dbSession.close()
            return "ERR_NOT_FOUND", 404
        question.title = request.form.get("title")
        question.category = request.form.get("category")
        if request.form.get("type") == "multipleChoice":
            type = questionType.multipleChoice
        elif request.form.get("type") == "trueFalse":
            type = questionType.trueFalse
        elif request.form.get("type") == "customAutomatic":
            type = questionType.custom
        elif request.form.get("type") == "customManual":
            type = questionType.external
        elif request.form.get("type") == "customMc":
            type = questionType.customMc
        else:
            type = questionType.text
        question.type = type
        question.gradingHint = request.form.get("hint")
        question.maxPoints = float(request.form.get("maxPoints"))
        if request.form.get("type") == "multipleChoice" or request.form.get("type") == "customMc":
            question.options = request.form.get("options")
            question.correctAnswer = request.form.get("correctAnswer")
        elif request.form.get("type") == "trueFalse":
            question.correctAnswer = request.form.get("correctAnswer")
        elif request.form.get("type") == "customAutomatic" or request.form.get("type") == "customMc":
            question.customGradingFunction = request.form.get("customFunction")
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        return "SUCCESS", 200
    elif request.method == "DELETE":
        question = dbSession.query(Question).filter(Question.id == id).first()
        if question is None:
            return "SUCCESS", 204
        dbSession.delete(question)
        try:
            dbSession.commit()
        except exc.SQLAlchemyError:
            dbSession.close()
            return "ERR_DATABASE", 500
        dbSession.close()
        if not fixQuestionIds(dbSession):
            return "ERR_DATABASE", 500
        return "SUCCESS", 200


@questionApi.route("/api/question/<id>/down", methods=["POST"])
@login_required
def moveQuestionDown(id):
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    id = int(id)
    thisQuestion = dbSession.query(Question).filter(Question.id == id).first()
    changeId = thisQuestion.displayId + 1
    replacerQuestion = dbSession.query(Question).filter(Question.displayId == changeId).first()
    if replacerQuestion == None:
        return "IS_HIGHEST", 500
    replacerQuestion.displayId = thisQuestion.displayId
    thisQuestion.displayId = changeId
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200


@questionApi.route("/api/question/<id>/up", methods=["POST"])
@login_required
def moveQuestionUp(id):
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    dbSession = database.createSession()
    id = int(id)
    thisQuestion = dbSession.query(Question).filter(Question.id == id).first()
    changeId = thisQuestion.displayId - 1
    if changeId <= 0:
        return "IS_LOWEST", 500
    replacerQuestion = dbSession.query(Question).filter(Question.displayId == changeId).first()
    replacerQuestion.displayId = thisQuestion.displayId
    thisQuestion.displayId = changeId
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200


@questionApi.route("/api/question/prepare", methods=["POST"])
@login_required
def prepareQuestions():
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    ids = json.loads(request.form.get("ids"))
    dbSession = database.createSession()
    questions = dbSession.query(Question).all()
    questionsPreparing = []
    for question in questions:
        if question.id in ids:
            currentPrepareQuestion = {}
            ids.remove(question.id)
            if question.state == questionState.prePreparation:
                question.state = questionState.inPreparation
                currentPrepareQuestion["displayId"] = question.displayId
                currentPrepareQuestion["questionId"] = question.id
                currentPrepareQuestion["category"] = question.category
                if question.type == questionType.multipleChoice or question.type == questionType.customMc:
                    currentPrepareQuestion["multipleChoice"] = len(json.loads(question.options))
                elif question.type == questionType.trueFalse:
                    currentPrepareQuestion["trueFalse"] = True
            else:
                return "ERR_WRONG_STATE", 400
            questionsPreparing.append(currentPrepareQuestion)
    if len(ids) > 0:
        return "ERR_INVALID_IDS", 400
    discord = discordDispatcher()
    discord.prepareQuestions(questionsPreparing)
    del discord
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200


@questionApi.route("/api/question/dispatch", methods=["POST"])
@login_required
def dispatchQuestions():
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    ids = json.loads(request.form.get("ids"))
    dbSession = database.createSession()
    questions = dbSession.query(Question).all()
    questionsAsking = []
    latestAnswerTime = datetime.datetime.now() + datetime.timedelta(seconds=int(request.form.get("time"))) + datetime.timedelta(seconds=10)
    for question in questions:
        if question.id in ids:
            currentSendQuestion = {}
            ids.remove(question.id)
            if question.state == questionState.waiting:
                question.state = questionState.asked
                question.latestAnswerTime = latestAnswerTime
                currentSendQuestion["question"] = question.title
                currentSendQuestion["displayId"] = question.displayId
                currentSendQuestion["questionId"] = question.id
                if question.type == questionType.multipleChoice:
                    currentSendQuestion["multipleChoice"] = question.options
                elif question.type == questionType.trueFalse:
                    currentSendQuestion["trueFalse"] = True
            else:
                return "ERR_WRONG_STATE", 400
            questionsAsking.append(currentSendQuestion)
    if len(ids) > 0:
        return "ERR_INVALID_IDS", 400
    m, s = divmod(int(request.form.get("time")), 60)
    if m > 0:
        time = str(m) + " Minuten und " + str(s) + " Sekunden"
    else:
        time = str(s) + " Sekunden"
    discord = discordDispatcher()
    discord.dispatchQuestions(questionsAsking, time)
    del discord
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200


@questionApi.route("/api/question/grade", methods=["POST"])
@login_required
def gradeQuestions():
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    ids = json.loads(request.form.get("ids"))
    dbSession = database.createSession()
    questions = dbSession.query(Question).all()
    for question in questions:
        if question.id in ids:
            ids.remove(question.id)
            if question.state == questionState.waitForGrading:
                question.state = questionState.inGrading
            else:
                dbSession.close()
                return "ERR_WRONG_STATE", 400
    if len(ids) > 0:
        dbSession.close()
        return "ERR_INVALID_IDS", 400
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    if autoGrade(json.loads(request.form.get("ids"))):
        return "SUCCESS", 200
    else:
        return "ERR_AUTO_GRADING", 500


@questionApi.route("/api/question/publish", methods=["POST"])
@login_required
def publishQuestions():
    if not permission.checkQuestionmaker(current_user.username):
        return "ACCESS_DENIED", 403
    ids = json.loads(request.form.get("ids"))
    dbSession = database.createSession()
    questions = dbSession.query(Question).all()
    for question in questions:
        if question.id in ids:
            ids.remove(question.id)
            if question.state == questionState.waitForPublishing:
                question.state = questionState.published
            else:
                dbSession.close()
                return "ERR_WRONG_STATE", 400
    if len(ids) > 0:
        dbSession.close()
        return "ERR_INVALID_IDS", 400
    try:
        dbSession.commit()
    except exc.SQLAlchemyError:
        dbSession.close()
        return "ERR_DATABASE", 500
    dbSession.close()
    return "SUCCESS", 200


@questionApi.route("/api/question/customgraders", methods=["GET"])
@login_required
def getCustomGraders():
    return jsonify(CustomGradingManager.getAvailableGraders()), 200


@questionApi.route("/api/question/<id>/csv", methods=["GET", "POST"])
@login_required
def externalGrading(id):
    if request.method == "GET":
        dbSession = database.createSession()
        question = dbSession.query(Question).filter(Question.id == id).first()
        answers = dbSession.query(Answer).filter(Answer.questionId == id).all()
        csv = ""
        for answer in answers:
            points = 0.0 if answer.points is None else answer.points
            csv += str(answer.id) + ";" + str(answer.teamId) + ";" + answer.value + ";" + str(points) + "\n"
        dbSession.close()
        return Response(csv, mimetype="text/csv", headers={"Content-disposition": "attachment; filename=question_" + str(question.displayId) + "_answers.csv"}), 200
    elif request.method == "POST":
        return "", 501