#!/usr/bin/env python3

# Message listener thread

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
from multiprocessing.connection import Listener


# Include modules
from modules.messageHandler import handleMessage
import config


# Class definition
class listenerThread(threading.Thread):
    def __init__(self, bot):
        threading.Thread.__init__(self)
        self.__adress = ("localhost", 18394)
        self.__listener = Listener(self.__adress, authkey=config.CONFIG_RPC_KEY.encode('utf_8'))
        self.__handlerThreads = []
        self.__bot = bot

    def run(self):
        while True:
            connection = self.__listener.accept()
            thread = threading.Thread(target=handleMessage, args=[connection, self.__bot])
            thread.start()
            self.__handlerThreads.append(thread)
            for thread in self.__handlerThreads:
                if not thread.is_alive():
                    self.__handlerThreads.remove(thread)
