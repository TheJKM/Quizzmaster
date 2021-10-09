#!/usr/bin/env python3

# User data model

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
from sqlalchemy import Column, Integer, Text, String, Boolean, ForeignKey, Enum


# Include modules
from modules.database import Base
from enums.registrationState import registrationState


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    isCaptain = Column(Boolean)
    email = Column(Text)
    teamId = Column(Integer, ForeignKey("team.id"))
    discordId = Column(Text)
    registrationStatus = Column(Enum(registrationState))

    # Create object
    def __init__(self, isCaptain, email=None, teamId=None):
        self.isCaptain = isCaptain
        self.registrationState = registrationState.discordPending
        if email is not None:
            self.email = email
        if teamId is not None:
            self.teamId = teamId
