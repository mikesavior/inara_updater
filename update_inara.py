#!/usr/bin/python

from EDMarketConnector import companion
import inara
import utils

settings = utils.get_settings()
companion_session = companion.Session()
inara_session = inara.Session()

try:
  companion_session.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
except companion.VerificationRequired:
  code = raw_input("Input Verification Code: ")
  companion_session.verify(code)

inara_session.inara_login(settings.get('inara', 'username'), settings.get('inara', 'password'))
inara_session._inara_handled_request(inara_session.post, inara.URL_BASE)

data = companion_session.query()
inara_session.inara_update_credits(data['commander']['credits'])
inara_session.inara_update_location(data['lastSystem']['name'])

companion_session.close()
