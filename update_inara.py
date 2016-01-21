#!/usr/bin/python

from elite_api import companion
from elite_api.inara import InaraSession
import utils

settings = utils.get_settings()
inara_session = InaraSession(settings.get('inara', 'username'), settings.get('inara', 'password'))

companion.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
data = companion.get_data()

inara_session.update_credits(data['commander']['credits'])
inara_session.update_location(data['lastSystem']['name'])

if utils.windows_detected():
  easygui.msgbox("Inara updated!")
else:
  print("Inara updated!")
