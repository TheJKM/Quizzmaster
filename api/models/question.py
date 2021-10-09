#!/usr/bin/env python3

# Question data model

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
from sqlalchemy import Column, Integer, Text, Enum, Float, DateTime
import json


# Include modules
from modules.database import Base
from enums.questionState import questionState
from enums.questionType import questionType


class Question(Base):
    __tablename__ = "question"
    id = Column(Integer, primary_key=True, autoincrement=True)
    displayId = Column(Integer)
    title = Column(Text)
    type = Column(Enum(questionType))
    state = Column(Enum(questionState))
    options = Column(Text)
    gradingHint = Column(Text)
    correctAnswer = Column(Integer)
    maxPoints = Column(Float)
    latestAnswerTime = Column(DateTime)

    # Create object
    def __init__(self, title, type, displayId, maxPoints):
        self.title = title
        self.type = type
        self.state = questionState.prePreparation
        self.options = json.dumps([])
        self.gradingHint = ""
        self.correctAnswer = -1
        self.displayId = displayId
        self.maxPoints = maxPoints
