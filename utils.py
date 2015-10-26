from ConfigParser import ConfigParser
from config import config
import os

def get_settings():
  """
  Try to read the settings from file into ConfigParser object.
  If the config file isn't found, initialize it and bail.
  """
  filename = os.path.join(config.app_dir, 'settings.conf')
  settings = ConfigParser()
  
  if os.path.isfile(filename):
    settings.read(filename)
  else:
    init_settings(settings, filename)

  return settings


def init_settings(settings, filename):
  settings.add_section('ed_companion')
  settings.add_section('inara')
  settings.set('ed_companion', 'username', '')
  settings.set('ed_companion', 'password', '')
  settings.set('inara', 'username', '')
  settings.set('inara', 'password', '')

  with open(filename, 'wb') as f:
    settings.write(f)

  raise Exception("Missing configuration. Please edit %s and run the program again." % filename)
