#!/usr/bin/env python3

# Management module for custom grading functions

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


# Include evaluators
from customGrading.whatDoMostSay import WhatDoMostSay


class CustomGradingManager():
    availableGraders = [
        {
            "mc": True,
            "class": WhatDoMostSay,
        }
    ]


    @staticmethod
    def getAvailableGraders():
        names = []
        for g in CustomGradingManager.availableGraders:
            names.append({
                "name": g["class"].__name__,
                "mc": g["mc"]
            })
        return names


    @staticmethod
    def getGraderClass(id):
        return CustomGradingManager.availableGraders[id]["class"]


    @staticmethod
    def getGradingFunctionByName(name):
        for grader in CustomGradingManager.availableGraders:
            if grader["class"].__name__ == name:
                return grader["class"]
        return None