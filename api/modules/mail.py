#!/usr/bin/env python3

# E-Mail sending module

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
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from socket import gaierror
import smtplib
import ssl


# Include modules
import config


# Class definition
class mail:

    @staticmethod
    def send(teamname, teamid, url, receiver):
        server = config.CONFIG_SMTP_SERVER
        login = config.CONFIG_SMTP_LOGIN
        sender = config.CONFIG_SMTP_SENDER
        password = config.CONFIG_SMTP_PASSWORD
        msg = MIMEMultipart('mixed')
        #msg["Content-Type"] = "text/plain; charset=utf-8"
        msg["Subject"] = config.CONFIG_CONFIRMATION_EMAIL_SUBJECT
        msg["From"] = config.CONFIG_CONFIRMATION_SENDER_READABLE_NAME + " <" + config.CONFIG_SMTP_SENDER + ">"
        msg["To"] = receiver
        content = config.CONFIG_CONFIRMATION_EMAIL_TEXT.format(teamname=teamname, teamid=teamid, url=url)
        part1 = MIMEText(content, "plain")
        msg.attach(part1)
        text = msg.as_string()
        try:
            with smtplib.SMTP_SSL(server, config.CONFIG_SMTP_PORT, context=ssl.create_default_context()) as server:
                server.login(login, password)
                server.sendmail(sender, receiver, text)
                return 0
        except (gaierror, ConnectionRefusedError):
            return -1
        except smtplib.SMTPServerDisconnected:
            return -2
        except smtplib.SMTPException as e:
            return -3
        except Exception as e:
            print(e)
            return -4
