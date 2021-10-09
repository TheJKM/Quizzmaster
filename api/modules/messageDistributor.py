#!/usr/bin/env python3

# Send a simple text message to the questions channel

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
import asyncio


# Include modules
from modules.discordHelper import getGuild
import config


# Required variables
eventloop = asyncio.get_event_loop()


# Distributor function
def distributeMessage(message, bot):
    execution = asyncio.run_coroutine_threadsafe(asyncSend(message, bot), eventloop)
    execution.result()

async def asyncSend(message, bot):
    guild = getGuild(bot)
    textChannel = guild.get_channel(int(config.CONFIG_QUESTIONS_CHANNEL))
    await textChannel.send(message)
