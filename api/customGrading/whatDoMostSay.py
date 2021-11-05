#!/usr/bin/env python3

# Custom evaluation class for "What do most say?" type of questions.

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
from customGrading.customGradingBase import CustomGradingBase


# Class definition
class WhatDoMostSay(CustomGradingBase):
    def executeGrading(self):
        options = {}
        # Step 1: Count the occurrences of each option
        for team in self.__dataset:
            if team["value"] is not None:
                if team["value"] in options:
                    options[team["value"]] += 1
                else:
                    options[team["value"]] = 1
        # Step 2: Determine which option(s) is / are the most used one(s)
        validAnswers = []
        mostCount = 0
        for option, count in options.items():
            if count > mostCount:  # More: remove all existing
                validAnswers = [option]
                mostCount = count
            elif count == mostCount:  # Same count: add to list
                validAnswers.append(option)
                mostCount = count
        # Step 3: Give full points to those who gave one of the valid answers, zero to all others
        for team in self.__dataset:
            if team["value"] is not None:
                team["points"] = self.__maxPoints if team["value"] in validAnswers else 0.0
