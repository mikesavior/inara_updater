from ConfigParser import ConfigParser
import os
import easygui
import platform

def get_config_dir():
  return os.path.join(os.path.expanduser('~'), '.ed_tools/')

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

def windows_detected():
  return platform.system() == 'Windows'

def _init_settings(settings, filename):
  settings.add_section('ed_companion')
  settings.add_section('inara')
  if windows_detected():
    _settings_prompt_gui(settings)
  else:
    _settings_prompt_cli(settings)
  
  with open(filename, 'wb') as f:
    settings.write(f)

def _settings_prompt_gui(settings):
  data = []
  easygui.multenterbox(
    "Enter your E:D and Inara credentials. You only need to do this once.",
    "Authentication Data",
    ["Elite Username (email address)", "Elite Password",
     "Inara Username", "Inara Password"],
    data
  )
  settings.set('ed_companion', 'username', data[0])
  settings.set('ed_companion', 'password', data[1])
  settings.set('inara', 'username', data[2])
  settings.set('inara', 'password', data[3])
  easygui.msgbox("To change your settings later, edit " + filename)

    
def _settings_prompt_cli(settings):
  settings.set('ed_companion', 'username', raw_input("Elite Username (email address): "))
  settings.set('ed_companion', 'password', raw_input("Elite Password: "))
  settings.set('inara', 'username', raw_input("Inara Username: "))
  settings.set('inara', 'password', raw_input("Inara Password: "))
  print "To change these settings later, edit " + filename
