#!/usr/bin/env python3

# Base class for writing a custom grading function

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


"""
How to write a custom grading function
Step 1: Create a new file in this directory, create a class inheriting CustomGradingBase
Step 2: Override the executeGrading function and implement your grading within it
Step 3: Import your class in the manager class, add it to the available methods
The base class (and so your inherited class) gets the full dataset before the grading function is called.
It has the following structure:
[
    {
        "id": 647831,
        "value": "Any string here",
        "points": 0.0
    },
    ...
]
Your job is easy: store the correct points.
Note: You can alter the value, but you MUST NOT ALTER THE ID!!!
The application takes care of storing the points back to the database.
Note that you can get any type of string as value! Take care of type errors. Your function should not raise exceptions.
If it does, the grading will fail, and no points are stored.
"""

# Base class definition
class CustomGradingBase():
    def __init__(self, dataset, maxPoints, correctAnswer):
        self.dataset = dataset
        self.maxPoints = maxPoints
        self.correctAnswer = correctAnswer


    def getResults(self):
        return self.dataset


    def executeGrading(self):
        pass