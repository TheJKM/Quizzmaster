#!/usr/bin/env python3

# Thread checking for expired questions

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
import threading
import time
import asyncio


# Include modules
from modules.database import database
from modules.timestampChecker import isTimestampValid
from modules.messageDistributor import distributeMessage
from models.question import Question
from enums.questionState import questionState
import config


# Required variables
eventloop = asyncio.get_event_loop()


# Class definition
class expirationCheckThread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.__bot = bot

    def run(self):
        while True:
            dbSession = database.createSession()
            questions = dbSession.query(Question).all()
            changed = False
            for question in questions:
                if question.state == questionState.asked and not isTimestampValid(question.latestAnswerTime):
                    question.state = questionState.waitForGrading
                    changed = True
            if changed:
                try:
                    dbSession.commit()
                    dbSession.close()
                except exc.SQLAlchemyError:
                    dbSession.close()
                distributeMessage(config.CONFIG_TIMEOUT_MESSAGE, self.__bot)
            dbSession.close()
            time.sleep(10)
