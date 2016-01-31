from ConfigParser import ConfigParser
import os
import platform

def get_config_dir(make=False):
  if platform.system() == 'Windows':
    config_suffix = os.path.join('AppData', 'Local', 'ed_tools')
  else:
    config_suffix = '.ed_tools'
  
  return os.path.join(os.path.expanduser('~'), config_suffix)

def get_settings(use_gui=True, parent=None):
  """
  Try to read the settings from file into ConfigParser object.
  If the config file isn't found, return None.
  """
  filename = os.path.join(get_config_dir(), 'settings.conf')
  settings = ConfigParser()
  
  if os.path.isfile(filename):
    settings.read(filename)
    return settings
  else:
    try:
      os.makedirs(get_config_dir())
    except:
      pass
    return None

def settings_update_ship(settings, ship_id, ship_name):
  # We include this check for backwards-compatibility.
  if not settings.has_section('ships'):
    settings.add_section('ships')

  settings.set('ships', str(ship_id), ship_name)
  write_settings(settings)

def update_settings(config_func, settings=None):
  """
  This function will initialize settings if it is None, call the passed function
  with the settings object as a parameter, then write the settings to the config
  file.
  """
  if settings is None:
    settings = ConfigParser()

  for section in ('ed_companion', 'inara', 'ships'):
    if not settings.has_section(section):
      settings.add_section(section)

  config_func(settings)
  write_settings(settings)

  return settings

def write_settings(settings):
  with open(os.path.join(get_config_dir(), 'settings.conf'), 'wb') as f:
    settings.write(f)
