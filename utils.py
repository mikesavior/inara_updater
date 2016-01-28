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

def update_settings(config_func, settings=None):
  """
  This function will initialize settings if it is None, call the passed function
  with the settings object as a parameter, then write the settings to the config
  file.
  """
  if settings is None:
    settings = ConfigParser()
    settings.add_section('ed_companion')
    settings.add_section('inara')

  config_func(settings)
    
  with open(os.path.join(get_config_dir(), 'settings.conf'), 'wb') as f:
    settings.write(f)

  return settings
