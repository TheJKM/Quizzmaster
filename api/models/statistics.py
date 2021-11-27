#!/usr/bin/env python3

# Settings data model

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
from sqlalchemy import Column, Text, Integer


# Include modules
from modules.database import Base


class Statistics(Base):
    __tablename__ = "statistics"
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(Text)
    value = Column(Integer)

    # Create object
    def __init__(self, key, value):
        self.key = key
        self.value = value