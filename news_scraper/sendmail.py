#!/usr/bin/python
# -*- coding: utf-8 -*-

import smtplib

display_name = '要闻快报'

template = """From: %s<%s>
To: %s
Subject: %s
Content-type: text/html

%s
"""

class GmailClient:
    def __init__(self, email_addr, password):
        self._email_addr = email_addr
        self._smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        self._smtp.ehlo()
        self._smtp.login(email_addr, password)


    def send(self, dest, subject, html_text):
        dest = dest + [ self._email_addr ]
        email_text = template % (display_name, self._email_addr, ", ".join(dest), subject, html_text)

        self._smtp.sendmail(self._email_addr, dest, email_text.encode('utf8'))
        #self._smtp.close()
