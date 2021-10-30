#!/usr/bin/env python3

# Message handler

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
import asyncio
import discord
import json


# Include modules
from modules.discordHelper import getGuild
from modules.database import database
from enums.messageType import messageType
from enums.questionState import questionState
from models.team import Team
from models.answer import Answer
from models.question import Question
import config


# Required variables
eventloop = asyncio.get_event_loop()


# Functions
def handleMessage(connection, bot):
    while True:
        try:
            message = connection.recv()
        except EOFError:  # Connection closed by the remote side
            break
        if message == "close":
            connection.close()
            break
        execution = asyncio.run_coroutine_threadsafe(asyncHandleMessage(message, bot), eventloop)
        execution.result()


async def asyncHandleMessage(message, bot):
    if message["type"] == messageType.userRegistration:
        guild = getGuild(bot)
        if message["isNewTeam"]:
            role = await guild.create_role(name="team_" + message["teamId"])
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                guild.me: discord.PermissionOverwrite(read_messages=True),
                role: discord.PermissionOverwrite(read_messages=True)
            }
            textChannel = await guild.create_text_channel(message["teamId"], overwrites=overwrites, topic="Text- und Antwortenkanal von " + message["teamName"] + " (" + message["teamId"] + ")")
            voiceChannel = await guild.create_voice_channel(message["teamId"], overwrites=overwrites, topic="Sprachkanal von " + message["teamName"] + " (" + message["teamId"] + ")")
            dbSession = database.createSession()
            team = dbSession.query(Team).filter(Team.displayId == message["teamId"]).first()
            team.textChannelId = textChannel.id
            team.voiceChannelId = voiceChannel.id
            try:
                dbSession.commit()
                dbSession.close()
            except exc.SQLAlchemyError:
                dbSession.close()
        else:
            role = discord.utils.get(getGuild(bot).roles, name="team_" + message["teamId"])
        user = await bot.fetch_user(message["userDiscordId"])
        member = guild.get_member(user.id)
        await member.add_roles(role)
    elif message["type"] == messageType.dispatchQuestions:
        guild = getGuild(bot)
        textChannel = guild.get_channel(int(config.CONFIG_QUESTIONS_CHANNEL))
        await textChannel.send(config.CONFIG_QUESTION_INTRODUCTION.format(time=message["time"]))
        for question in message["questions"]:
            await textChannel.send("Frage " + str(question["displayId"]) + ": " + question["question"])
            if "multipleChoice" in question:
                await textChannel.send("Wählt aus den folgenden Antwortmöglichkeiten:")
                i = 1
                for option in json.loads(question["multipleChoice"]):
                    await textChannel.send("Option " + str(i) + ": " + option)
                    i += 1
            elif "trueFalse" in question:
                await textChannel.send("Wahr oder falsch?")
    elif message["type"] == messageType.prepareQuestions:
        guild = getGuild(bot)
        dbSession = database.createSession()
        teams = dbSession.query(Team).all()
        for team in teams:
            textChannel = guild.get_channel(int(team.textChannelId))
            for question in message["questions"]:
                sentMessage = await textChannel.send("Dummy für \"" + str(question["category"]) + "\" (" + str(question["displayId"]) + ").")
                answer = Answer(question["questionId"], team.id, sentMessage.id)
                dbSession.add(answer)
                if "multipleChoice" in question:
                    emojis = ['1️⃣', '2️⃣', '3️⃣', '4️⃣', '5️⃣', '6️⃣', '7️⃣', '8️⃣', '9️⃣', '🔟']
                    for i in range(int(question["multipleChoice"])):
                        await sentMessage.add_reaction(emojis[i])
                elif "trueFalse" in question:
                    await sentMessage.add_reaction('\N{THUMBS UP SIGN}')
                    await sentMessage.add_reaction('\N{THUMBS DOWN SIGN}')
        for question in message["questions"]:
            q = dbSession.query(Question).filter(Question.id == question["questionId"]).first()
            q.state = questionState.waiting
        try:
            dbSession.commit()
            dbSession.close()
        except exc.SQLAlchemyError:
            dbSession.close()
