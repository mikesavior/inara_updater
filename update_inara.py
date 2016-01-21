#!/usr/bin/python

from edmc import companion
from inara.inara import InaraSession
import utils

settings = utils.get_settings()
companion_session = companion.Session()
inara_session = InaraSession(settengs.get('inara', 'username'), settings.get('inara', 'password'))

try:
  companion_session.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
except companion.VerificationRequired:
  code = raw_input("Input Verification Code: ")
  companion_session.verify(code)

data = companion_session.query()
inara_session.update_credits(data['commander']['credits'])
inara_session.update_location(data['lastSystem']['name'])

companion_session.close()
