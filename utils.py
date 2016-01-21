from ConfigParser import ConfigParser
import os

def get_config_dir():
  return os.path.join(path.expanduser('~'), '.ed_tools/')

def get_settings():
  """
  Try to read the settings from file into ConfigParser object.
  If the config file isn't found, initialize it.
  """
  filename = os.path.join(get_config_dir(), 'settings.conf')
  settings = ConfigParser()
  
  if os.path.isfile(filename):
    settings.read(filename)
  else:
    _init_settings(settings, filename)

  return settings


def _init_settings(settings, filename):
  settings.add_section('ed_companion')
  settings.add_section('inara')
  settings.set('ed_companion', 'username', raw_input("Elite Username (email address): "))
  settings.set('ed_companion', 'password', raw_input("Elite Password: "))
  settings.set('inara', 'username', raw_input("Inara Username: "))
  settings.set('inara', 'password', raw_input("Inara Password: "))
  print "To change these settings later, edit " + filename
  
  with open(filename, 'wb') as f:
    settings.write(f)
