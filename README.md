# Quizzmaster Discord Bot

## WARNING - THIS IS BETA SOFTWARE!
Quizzmaster has yet to prove its functionality. We expect a stable, tested version by the end of this year. Stay tuned!

## What is this?
Quizzmaster is a Discord bot for organizing digital pub quizzes on a Discord server.

## Why is this so awesome?
It automizes registration, question distrubution and answer collection, can grade multiple-choice and true-false questions automatically, and helps by grading free text questions. It provides a live scoreboard and a backoffice for managing questions and answers. Organizing a digital pub quiz is now easier than ever before!

## Requirements
Quizzmaster backend is written in Python using Flask, SQLAlchemy and discord-py.
- Python 3.8 or newer with Pip3
- A SQL database 
    - I recommend using MariaDB, as I'm using it in our instance.
    - SQLite is working, but only for development purposes because of performance issues.
    - In theory, all databases supported by SQLAlchemy should work, but they are untested!
- Supported operating systems:
    - Linux (tested on Ubuntu 20.04 and Manjaro, for development and production)
    - macOS (tested on 11.3 or newer, only for development)
    - Note: Windows is NOT supported! Expect bugs and non-working features. Please do not ask about Windows specific fixes.

The frontend utilizes Framework7. It compiles to static HTML/JS. For frontend development, you'll need:
- NodeJS and NPM

## Setup
Setup instructions will be added when Quizzmastes leaves its beta phase.

## Contributing
I appreciate any contribution!
- If you find a bug or want to provide some feedback/ideas, please open an issue.
- If you want to contribute code, please open a pull request.

## License
Quizzmaster Discord bot for digital pub quizzes  
Copyright (C) 2021 Johannes Kreutz.  

This program is free software: you can redistribute it and/or modify  
it under the terms of the GNU Affero General Public License as  
published by the Free Software Foundation, either version 3 of the  
License, or (at your option) any later version.  

This program is distributed in the hope that it will be useful,  
but WITHOUT ANY WARRANTY; without even the implied warranty of  
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the  
GNU Affero General Public License for more details.  

You should have received a copy of the GNU Affero General Public License  
along with this program.  If not, see <https://www.gnu.org/licenses/>.
