#!/usr/bin/python

from edmc import companion
from inara.inara import InaraSession
import utils

settings = utils.get_settings()
companion_session = companion.Session()
inara_session = InaraSession(settings.get('inara', 'username'), settings.get('inara', 'password'))

try:
  companion_session.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
except companion.VerificationRequired:
  if utils.windows_detected():
    code = easygui.enterbox("Input Verification Code (check your email)",
                            "Verification Required")
  else:
    code = raw_input("Input Verification Code (check your email): ")
  companion_session.verify(code)

data = companion_session.query()
companion_session.close()

inara_session.update_credits(data['commander']['credits'])
inara_session.update_location(data['lastSystem']['name'])

if utils.windows_detected():
  easygui.msgbox("Inara updated!")
else:
  print("Inara updated!")
