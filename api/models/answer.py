#!/usr/bin/env python3

# Answer data model

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
from sqlalchemy import Column, Integer, Text, ForeignKey, Float, Boolean


# Include modules
from modules.database import Base


class Answer(Base):
    __tablename__ = "answer"
    id = Column(Integer, primary_key=True, autoincrement=True)
    questionId = Column(Integer, ForeignKey("question.id", ondelete='CASCADE'))
    teamId = Column(Integer, ForeignKey("team.id"))
    value = Column(Text)
    points = Column(Float)
    messageId = Column(Text)
    graderAssigned = Column(Boolean)

    # Create object
    def __init__(self, questionId, teamId, messageId):
        self.questionId = questionId
        self.teamId = teamId
        self.messageId = messageId
