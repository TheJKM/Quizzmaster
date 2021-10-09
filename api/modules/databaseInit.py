#!/usr/bin/env python3

# Database initializer

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


# Include modules
from models.settings import Settings
from modules.database import database


def initDatabase():
    wanted = {
        "teamRegistrationOpen": "true",
    }
    dbSession = database.createSession()
    setting = dbSession.query(Settings).all()
    for s in setting:
        if s.key in wanted.keys():
            del wanted[s.key]
    for key in wanted.keys():
        s = Settings(key, wanted[key])
        dbSession.add(s)
    try:
        dbSession.commit()
        dbSession.close()
        return True
    except exc.SQLAlchemyError:
        dbSession.close()
        return False
