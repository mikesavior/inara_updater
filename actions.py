"""
This module mostly serves as a shim between the elite_api library and the rest of our program.
"""

from elite_api import companion
from elite_api.inara import InaraSession


def do_logins(settings):
  inara_session = InaraSession(settings.get('inara', 'username'), settings.get('inara', 'password'))
  companion.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
  return inara_session


def update_inara(inara_session):
  data = companion.get_data()
  inara_session.update_credits(data['commander']['credits'])
  inara_session.update_location(data['lastSystem']['name'])
