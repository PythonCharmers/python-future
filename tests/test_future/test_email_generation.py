# -*- coding: utf-8 -*-
"""Tests for email generation."""

from __future__ import unicode_literals

from future.backports.email.mime.multipart import MIMEMultipart
from future.backports.email.mime.text import MIMEText
from future.backports.email.utils import formatdate
from future.tests.base import unittest


class EmailGenerationTests(unittest.TestCase):
    def test_email_custom_header_can_contain_unicode(self):
        msg = MIMEMultipart()
        alternative = MIMEMultipart('alternative')
        alternative.attach(MIMEText('Plain content with Únicødê', _subtype='plain', _charset='utf-8'))
        alternative.attach(MIMEText('HTML content with Únicødê', _subtype='html', _charset='utf-8'))
        msg.attach(alternative)

        msg['Subject'] = 'Subject with Únicødê'
        msg['From'] = 'sender@test.com'
        msg['To'] = 'recipient@test.com'
        msg['Date'] = formatdate(None, localtime=True)
        msg['Message-ID'] = 'anIdWithÚnicødêForThisEmail'

        msg_lines = msg.as_string().split('\n')
        self.assertEqual(msg_lines[2], 'Subject: =?utf-8?b?U3ViamVjdCB3aXRoIMOabmljw7hkw6o=?=')
        self.assertEqual(msg_lines[6], 'Message-ID: =?utf-8?b?YW5JZFdpdGjDmm5pY8O4ZMOqRm9yVGhpc0VtYWls?=')
        self.assertEqual(msg_lines[17], 'UGxhaW4gY29udGVudCB3aXRoIMOabmljw7hkw6o=')
        self.assertEqual(msg_lines[24], 'SFRNTCBjb250ZW50IHdpdGggw5puaWPDuGTDqg==')
