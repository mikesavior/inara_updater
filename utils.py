from ConfigParser import ConfigParser
import os
import easygui
import platform

def get_config_dir(make=False):
  if platform.system() == 'Windows':
    config_suffix = os.path.join('AppData', 'Local', 'ed_tools')
  else:
    config_suffix = '.ed_tools'
  
  return os.path.join(os.path.expanduser('~'), config_suffix)

def get_settings(use_gui=True):
  """
  Try to read the settings from file into ConfigParser object.
  If the config file isn't found, initialize it.
  """
  filename = os.path.join(get_config_dir(), 'settings.conf')
  settings = ConfigParser()
  
  if os.path.isfile(filename):
    settings.read(filename)
  else:
    try:
      os.makedirs(get_config_dir())
    except:
      pass

    settings = init_settings(use_gui)

  return settings

def init_settings(gui=True):
  settings = ConfigParser()
  settings.add_section('ed_companion')
  settings.add_section('inara')
  if gui:
    _settings_prompt_gui(settings)
  else:
    _settings_prompt_cli(settings)
    print "To change these settings later, edit " + filename

  with open(os.path.join(get_config_dir(), 'settings.conf'), 'wb') as f:
    settings.write(f)

  return settings

def _settings_prompt_gui(settings):
  data = []
  data = easygui.multenterbox(
    "Enter your E:D and Inara credentials. You only need to do this once.",
    "Authentication Data",
    ["Elite Username (email address)", "Elite Password",
     "Inara Username", "Inara Password"]
  )

  for i in range(4):
    if data[i].strip() == '':
      easygui.msgbox("You must provide data for all fields.")
      _settings_prompt_gui(settings)
      return
  
  settings.set('ed_companion', 'username', data[0].strip())
  settings.set('ed_companion', 'password', data[1].strip())
  settings.set('inara', 'username', data[2].strip())
  settings.set('inara', 'password', data[3].strip())

    
def _settings_prompt_cli(settings):
  settings.set('ed_companion', 'username', raw_input("Elite Username (email address): "))
  settings.set('ed_companion', 'password', raw_input("Elite Password: "))
  settings.set('inara', 'username', raw_input("Inara Username: "))
  settings.set('inara', 'password', raw_input("Inara Password: "))
