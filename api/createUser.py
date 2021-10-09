#!/usr/local/env python3

# User creation helper script

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
from passlib.hash import bcrypt
import sys


# Include modules
from modules.database import database
from models.backendUser import BackendUser


if not len(sys.argv) == 3:
    print("Usage: python3 createAdminUser.py <username> <password>")
    sys.exit(0)

username = sys.argv[1]
password = bcrypt.hash(sys.argv[2])

dbSession = database.createSession()
user = BackendUser(username, password, False, False, True)
dbSession.add(user)
try:
    dbSession.commit()
except exc.SQLAlchemyError:
    dbSession.close()
    print("User creation failed.")
dbSession.close()
print("User successfully created.")
