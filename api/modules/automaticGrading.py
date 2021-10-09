#!/usr/bin/env python3

# Automatic grading for multiple choice and true false questions

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
from sqlalchemy import exc


# Include modules
from models.question import Question
from models.answer import Answer
from modules.database import database
from enums.questionState import questionState
from enums.questionType import questionType


# Grading function
def autoGrade(ids):
    dbSession = database.createSession()
    questions = dbSession.query(Question).filter(Question.state == questionState.inGrading).all()
    for question in questions:
        if question.id in ids:
            if question.type == questionType.multipleChoice or question.type == questionType.trueFalse:
                answers = dbSession.query(Answer).filter(Answer.questionId == question.id).all()
                for answer in answers:
                    if answer.value == None:
                        answer.points = float(0)
                    elif int(answer.value) == question.correctAnswer:
                        answer.points = question.maxPoints
                    else:
                        answer.points = float(0)
                question.state = questionState.waitForPublishing
    try:
        dbSession.commit()
        dbSession.close()
        return True
    except exc.SQLAlchemyError:
        dbSession.close()
        return False
