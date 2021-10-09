#!/usr/bin/env python3

# Remove holes in the question ids

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


# Include modules
from models.question import Question


def fixQuestionIds(session):
    startId = 1
    questions = session.query(Question).order_by(Question.displayId)
    for q in questions:
        if not q.displayId == startId:
            q.displayId = startId
        startId += 1
    try:
        session.commit()
        return True
    except exc.SQLAlchemyError:
        session.close()
        return False
