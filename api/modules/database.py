#!/usr/bin/env python3

# Database connector

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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.pool import NullPool


# Include modules
import config


# Create the declarative base object
Base = declarative_base()


# Class definition
class database:

    # Create connection
    def __init__(self, test=False):
        self.engine = create_engine(config.CONFIG_DATABASE_PATH, pool_recycle=60, poolclass=NullPool)

    # Create tables
    def createTables(self):
        Base.metadata.create_all(self.engine)

    # Return engine
    def getEngine(self):
        return self.engine

    # Create a session
    @staticmethod
    def createSession():
        db = globalConnection
        db.createTables()
        sessionFactory = sessionmaker(bind=db.getEngine())
        sessionClass = scoped_session(sessionFactory)
        session = sessionClass()
        return session

# Create the global database connection
globalConnection = database()
