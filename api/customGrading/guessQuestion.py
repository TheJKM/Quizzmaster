#!/usr/bin/env python3

# Custom evaluation class for guess questions.

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
import re


# Include modules
from customGrading.customGradingBase import CustomGradingBase


# Class definition
class GuessQuestion(CustomGradingBase):
    def executeGrading(self):
        # Step 1: Determine the best answer
        answers = []
        sum_valid_answers = 0
        valid_answers = 0
        for team in self.dataset:
            try:
                value_float = self.extractFloats(team["value"])
                sum_valid_answers += value_float
                valid_answers += 1
            except (ValueError, TypeError) as error:
                value_float = -1e10
            answers.append(value_float)
        mean_guess = sum_valid_answers / valid_answers

        # Step 2: Determine which answers were best
        differences = []
        for ans in answers:
            differences.append(abs(ans-mean_guess))
        differences.sort()

        # Step 3: Set intervals for points
        # Currently set to top 50% receiving points, in equally sized clusters in steps of 0.5 points
        # With the assumption that every cluster includes at least one team
        point_range = int(self.maxPoints*2)
        point_size = round(valid_answers/(2*point_range)+0.5)

        # Step 4: Determine the cutoffs for each cluster given all answers
        cutoffs = []
        index = -1
        for i in range(point_range):
            index += point_size
            cutoffs.append(differences[index])

        # Step 5: Assign the points to each team given the selected clusters
        for team in self.dataset:
            try:
                value_float = self.extractFloats(team["value"])
            except (ValueError, TypeError) as error:
                value_float = -1e10
            difference = abs(value_float-mean_guess)
            for i in range(len(cutoffs)):
                if difference <= cutoffs[i]:
                    team["points"] = self.maxPoints - i*0.5
                    break
            if difference > cutoffs[-1]:
                team["points"] = 0.0


    def extractFloats(self, input):
        try:
            searchFloats = re.findall(r"[-+]?\d*\.\d+|\d+", input.replace(",", "."))
            if len(searchFloats) == 0:
                return -1e10
            return float(searchFloats[0])
        except:
            return -1e10