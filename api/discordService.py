#!/usr/bin/env python3

# Quizzmaster discord bot for running digital pubquizzes through discord
# Discord Service listener

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
import discord
from discord.ext import commands
import sys


# Include modules
import config
from modules.listenerThread import listenerThread
from modules.expirationCheckThread import expirationCheckThread
from modules.eventEvaluator import evaluateTextAnswer, evaluateReactionAnswer
from modules.databaseInit import initDatabase


# Import data models to enable scheme creation
from models.user import User
from models.team import Team
from models.question import Question
from models.answer import Answer
from models.backendUser import BackendUser
from models.settings import Settings


# Defint the bot description
description = "Quizzmaster is the ultimate Discord Bot for running online pub quizes. Made with ❤️ and Code by Johannes Kreutz."


# Define required discord intents
intents = discord.Intents.default()
intents.members = True


# Create bot
bot = commands.Bot(command_prefix="/", description=description, intents=intents)


# Bot events
@bot.event
async def on_ready():
    print("Bot is up and running: User " + bot.user.name + ", ID " + str(bot.user.id))


@bot.event
async def on_message(message):
    if message.reference is not None and not message.author.id == bot.user.id:
        await evaluateTextAnswer(message);


@bot.event
async def on_raw_reaction_add(payload):
    if not payload.user_id == bot.user.id:
        message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
        user = payload.member
        await evaluateReactionAnswer(reaction, message, user, True)


@bot.event
async def on_raw_reaction_remove(payload):
    message = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)
    user = payload.member
    await evaluateReactionAnswer(reaction, message, user)


# Start listener
listener = listenerThread(bot)
listener.daemon = True
listener.start()


# Start expiration checker
checker = expirationCheckThread(bot)
checker.daemon = True
checker.start()


# Init database
initDatabase()


# Start bot
bot.run(config.CONFIG_BOT_TOKEN)
