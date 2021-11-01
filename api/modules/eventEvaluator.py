#!/usr/bin/env python3

# Evaluation of discord events

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
from modules.database import database
from enums.questionType import questionType
from enums.questionState import questionState
from models.question import Question
from models.answer import Answer
import config


# Evaluator function for text answers
async def evaluateTextAnswer(message):
    dbSession = database.createSession()
    answers = dbSession.query(Answer).filter(Answer.messageId == str(message.reference.message_id)).all()
    if len(answers) == 1:
        answer = answers[0]
        question = dbSession.query(Question).filter(Question.id == answer.questionId).first()
        if question is not None:
            if question.state == questionState.asked:
                if question.type == questionType.text:
                    answer.value = message.content
                    try:
                        dbSession.commit()
                    except exc.SQLAlchemyError:
                        pass
                else:
                    await message.reply(config.CONFIG_TEXT_FOR_MC_TF, mention_author=False)
            elif question.state.value < questionState.asked.value:
                await message.reply(config.CONFIG_TOO_EARLY_MESSAGE, mention_author=False)
            else:
                await message.reply(config.CONFIG_TIMEOUT_MESSAGE, mention_author=False)
    dbSession.close()


# Evaluator function for emoji reactions
async def evaluateReactionAnswer(reaction, message, user, add=False):
    dbSession = database.createSession()
    answers = dbSession.query(Answer).filter(Answer.messageId == str(message.id)).all()
    if len(answers) == 1:
        answer = answers[0]
        question = dbSession.query(Question).filter(Question.id == answer.questionId).first()
        if question is not None:
            if question.state == questionState.asked:
                if question.type == questionType.multipleChoice:
                    emojis = {'1️⃣': 0, '2️⃣': 0, '3️⃣': 0, '4️⃣': 0, '5️⃣': 0, '6️⃣': 0, '7️⃣': 0, '8️⃣': 0, '9️⃣': 0, '🔟': 0}
                    for reaction in message.reactions:
                        for emoji in emojis.keys():
                            if emoji == reaction.emoji:
                                emojis[emoji] = reaction.count
                    highest = None
                    highestVal = 0
                    i = 0
                    for emoji in emojis.keys():
                        if emojis[emoji] > highestVal:
                            highest = i
                            highestVal = emojis[emoji]
                        elif emojis[emoji] == highestVal:
                            highest = None
                        i += 1
                    answer.value = highest
                    try:
                        dbSession.commit()
                    except exc.SQLAlchemyError:
                        pass
                elif question.type == questionType.trueFalse:
                    up = 0
                    down = 0
                    for reaction in message.reactions:
                        if reaction.emoji == '\N{THUMBS UP SIGN}':
                            up += reaction.count
                        elif reaction.emoji == '\N{THUMBS DOWN SIGN}':
                            down += reaction.count
                    if up < down:
                        answer.value = 0
                    elif up > down:
                        answer.value = 1
                    else:
                        answer.value = None
                    try:
                        dbSession.commit()
                    except exc.SQLAlchemyError:
                        pass
            elif question.state.value < questionState.asked.value and add:
                await reaction.remove(user)
                await message.reply(config.CONFIG_TOO_EARLY_MESSAGE, mention_author=False)
            elif add:
                await reaction.remove(user)
                await message.reply(config.CONFIG_TIMEOUT_MESSAGE, mention_author=False)
    dbSession.close()
