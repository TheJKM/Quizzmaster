#!/usr/bin/env python3

# Answer module for bot commands

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
import json
from sqlalchemy.sql import func


# Include modules
from modules.database import database
from models.team import Team
from models.answer import Answer
from models.question import Question
from enums.questionState import questionState
from enums.questionType import questionType
import config


# Answer current score command
async def answerCurrentScore(sourceMessage):
    if (id := getCommandTeamInternalId(sourceMessage.channel)) is not None:
        dbSession = database.createSession()
        questions = dbSession.query(Question).filter(Question.state == questionState.published).all()
        publishedQuestionIds = []
        for q in questions:
            publishedQuestionIds.append(q.id)
        answers = dbSession.query(func.sum(Answer.points).label("score")).filter(Answer.teamId == id).filter(Answer.questionId.in_(publishedQuestionIds)).first()
        points = answers[0] if answers[0] is not None else 0
        await sourceMessage.reply(config.CONFIG_COMMAND_SCORE_MESSAGE.format(points=points), mention_author=False)
        dbSession.close()
    else:
        await sourceMessage.reply(config.CONFIG_COMMAND_OUTSIDE_TEAM_CHANNEL_MESSAGE, mention_author=False)


# Answer team answers command
async def answerTeamAnswers(sourceMessage):
    if (id := getCommandTeamInternalId(sourceMessage.channel)) is not None:
        dbSession = database.createSession()
        answers = dbSession.query(Question, Answer).join(Question, Question.id == Answer.questionId).filter(Answer.teamId == id).all()
        text = "Eure bisherigen Antworten:\n"
        for a in answers:
            question = a[0]
            answer = a[1]
            if question.state.value >= questionState.asked.value:
                if answer.value is None:
                    text += "Frage {questionnr} ({title}): (Keine Antwort abgegeben).\n".format(questionnr=question.displayId, title=question.title)
                elif question.type == questionType.multipleChoice or question.type == questionType.customMc:
                    numeric = int(answer.value) + 1
                    options = json.loads(question.options)
                    full = options[int(answer.value)]
                    text += "Frage {questionnr} ({title}): Option {numeric} ({answer})\n".format(questionnr=question.displayId, title=question.title, numeric=numeric, answer=full)
                elif question.type == questionType.trueFalse:
                    type = "wahr" if answer.value == "1" else "falsch"
                    text += "Frage {questionnr} ({title}): {type}.\n".format(questionnr=question.displayId, title=question.title, type=type)
                else:
                    text += "Frage {questionnr} ({title}): {answer}\n".format(questionnr=question.displayId, title=question.title, answer=answer.value)
        await sourceMessage.reply(text, mention_author=False)
        dbSession.close()
    else:
        await sourceMessage.reply(config.CONFIG_COMMAND_OUTSIDE_TEAM_CHANNEL_MESSAGE, mention_author=False)


# Helper to get the internal id of the team who issued the command
def getCommandTeamInternalId(channel):
    dbSession = database.createSession()
    team = dbSession.query(Team).filter(Team.textChannelId == channel.id).first()
    if team is None:
        dbSession.close()
        return None
    else:
        dbSession.close()
        return team.id
