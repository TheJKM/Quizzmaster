#!/usr/bin/env python3

# Discord service message dispatcher

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
from multiprocessing.connection import Client


# Include modules
import config
from enums.messageType import messageType


# Class definition
class discordDispatcher:

    # Create client
    def __init__(self):
        self.__adress = ("localhost", 18394)
        self.__client = Client(self.__adress, authkey=config.CONFIG_RPC_KEY.encode('utf_8'))

    # Close connection
    def __del__(self):
        self.__client.close()

    # Create a channel
    def createChannel(self, teamId, isNewTeam, userDiscordId, teamName):
        request = {
            "type": messageType.userRegistration,
            "teamId": teamId,
            "isNewTeam": isNewTeam,
            "userDiscordId": userDiscordId,
            "teamName": teamName,
        }
        self.__client.send(request)

    # Dispatch questions
    def dispatchQuestions(self, questions, time):
        request = {
            "type": messageType.dispatchQuestions,
            "time": time,
            "questions": questions,
        }
        self.__client.send(request)

    # Prepare questions
    def prepareQuestions(self, questions, team=None):
        request = {
            "type": messageType.prepareQuestions,
            "questions": questions,
        }
        if team is not None:
            request["team"] = team
        self.__client.send(request)
