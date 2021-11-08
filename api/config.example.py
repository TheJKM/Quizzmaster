#!/usr/bin/env python3

# Quizzmaster configuration file

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


# Database connection
CONFIG_DATABASE_PATH = "sqlite:////tmp/test.db"

# File for storing the cookie key
CONFIG_SECRET_KEY = "SecretKey.txt"

# Deployment settings (required for redirection in OAuth2 flow)
CONFIG_BASE_DOMAIN = "http://localhost:8080"

# OAuth2 secrets
CONFIG_OAUTH2_CLIENT_ID = "REPLACE_ID"
CONFIG_OAUTH2_CLIENT_SECRET = "REPLACE_TOKEN"

# Bot token
CONFIG_BOT_TOKEN = "REPLACE_TOKEN"

# Discord API
CONFIG_DISCORD_API_BASE = "https://discord.com/api"

# Discord Server
CONFIG_DISCORD_SERVER = "REPLACE_ID"

# Channel ID for questions channel
CONFIG_QUESTIONS_CHANNEL = "REPLACE_QUESTIONS_CHANNEL_ID"

# Maximum number of teams
CONFIG_MAX_TEAM_COUNT = 230

# E-Mail credentials
CONFIG_SMTP_SERVER = ""
CONFIG_SMTP_LOGIN = ""
CONFIG_SMTP_SENDER = ""
CONFIG_SMTP_PASSWORD = ""
CONFIG_SMTP_PORT = 465

# Additional parameters for registration (array)
CONFIG_REGISTER_QUESTIONS = [
    {
        "text": "Erklärung zu 1",
        "question": "Frage 1"
    },
    {
        "text": "Erklärung zu 2",
        "question": "Frage 2"
    },
    {
        "text": "Erklärung zu 3",
        "question": "Frage 3"
    },
]
CONFIG_LANDING_PAGE_TITLE = "Quizzmaster Anmeldung"
CONFIG_LANDING_PAGE_TEXT = "Willkommen bei der Anmeldung zu Test Pubquiz."

# RPC Communication key between web api server and discord service
CONFIG_RPC_KEY = "ANYTHING_RANDOM_HERE"

# Content for confirmation email. Available variables: teamname, teamid, url
CONFIG_CONFIRMATION_EMAIL_TEXT = """\
Hallo {teamname},

vielen Dank für deine Anmeldung! Deinem Team wurde die Team-ID {teamid} zugewiesen. Du wurdest bereits unserem Discord-Server hinzugefügt. Dein Team kann mit dem folgenden Link ebenfalls dem Discord-Server beitreten: {url}. Alternativ können weitere Teammitglieder über die Anmeldeseite nach Eingabe der Team-ID beitreten.

Viele Grüße
Quizzmaster (Bot)

"""
CONFIG_CONFIRMATION_EMAIL_SUBJECT = "Quizzmaster: Anmeldung erfolgreich"
CONFIG_CONFIRMATION_SENDER_READABLE_NAME = "Quizzmaster Team"

# Question asking instroduction line
CONFIG_QUESTION_INTRODUCTION = "Ihr habt {time} Zeit für die Beantwortung der folgenden Fragen. Freitext-Fragen beantwortet ihr bitte mit der Antwort-Funktion von Discord im Antworten-Channel eures Teams. Für Multiple-Choice- oder Wahr-Falsch-Fragen werden Reaktionsmöglichkeiten angeboten, es gewinnt die Wahl mit der höchsten Anzahl an Klicks (bei Gleichstand wird keine Anwort gezählt)."

# Time out message
CONFIG_TIMEOUT_MESSAGE = "⏰ Die Antwortzeit ist abgelaufen, es werden keine Antworten mehr akzeptiert."
CONFIG_TIMEOUT_ANSWER_MESSAGE = "⏰ Die Antwortzeit für diese Frage ist abgelaufen, deine Antwort wurde nicht gezählt."
CONFIG_TOO_EARLY_MESSAGE = "Diese Frage wurde noch nicht gestellt. Bitte antworte erneut, sobald die Frage gestellt wurde. Deine Antwort wurde nicht gezählt."
CONFIG_TEXT_FOR_MC_TF = "Dies ist eine Multiple-Choice- oder Wahr-Falsch-Frage, die mittels Klick auf ein Emoji beantwortet wird. Deine Textantwort wurde nicht gezählt."
CONFIG_COMMAND_OUTSIDE_TEAM_CHANNEL_MESSAGE = "Dieser Befehl funktioniert nur in deinem Team-Channel."
CONFIG_COMMAND_SCORE_MESSAGE = "Dein Team hat bisher {points} Punkte erreicht. Dabei sind nur bereits vollständig ausgewertete Fragen berücksichtigt."

# Signup consent text
CONFIG_SIGNUP_CONSENT = "Hinweise zum Datenschutz: Das Pubquiz findet auf Discord statt. Auf dem Discord-Server existieren Textkanäle, die für alle Teilnehmer*innen zugänglich sind. Ich stimme zu, dass sämtliche Inhalte (einschließlich Bilder, Videos sowie andere Dateien), die ich außerhalb meines Team-Kanals poste, im Rahmen des Pubquiz uneingeschränkt verwendet werden können. Insbesondere kann Bild- und Videomaterial im Livestream gezeigt werden. Ich garantiere, dass ich die Zustimmung zur Verwendung von allen auf Bild- und Videomaterial zu sehenden Personen erhalten habe."
