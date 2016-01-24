from ConfigParser import ConfigParser
import os
import Tkinter as tk
import tkSimpleDialog, tkMessageBox
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

    settings = update_settings(use_gui, parent)

  return settings


def update_settings(gui=True, parent=None, settings=None):
  if settings is None:
    settings = ConfigParser()
    settings.add_section('ed_companion')
    settings.add_section('inara')
  if gui:
    dialog = ConfigDialog(parent, settings)
  else:
    _settings_prompt_cli(settings)
    print "To change these settings later, edit " + filename

  with open(os.path.join(get_config_dir(), 'settings.conf'), 'wb') as f:
    settings.write(f)

  return settings


def _settings_prompt_cli(settings):
  settings.set('ed_companion', 'username', raw_input("Elite Username (email address): "))
  settings.set('ed_companion', 'password', raw_input("Elite Password: "))
  settings.set('inara', 'username', raw_input("Inara Username: "))
  settings.set('inara', 'password', raw_input("Inara Password: "))


class ConfigDialog(tkSimpleDialog.Dialog):
  def __init__(self, parent, settings, title="Authentication Data"):
    self.settings = settings
    self.entries = []
    self.data = []
    tkSimpleDialog.Dialog.__init__(self, parent, title)
    
  def body(self, parent):
    i = 0
    values = []

    for section, value in (('ed_companion', 'username'),
                           ('ed_companion', 'password'),
                           ('inara', 'username'),
                           ('inara', 'password')):
      if self.settings.has_option(section, value):
        values.append(self.settings.get(section, value))
      else:
        values.append("")
        
    for field in ("Elite Username (email address):",
                  "Elite Password:",
                  "Inara Username:",
                  "Inara Password:"):
      label = tk.Label(parent, text=field)
      label.grid(row=i, column=0, sticky=tk.W)
      entry = tk.Entry(parent, width=30)
      entry.insert(0, values[i])
      entry.grid(row=i, column=1, sticky=tk.E)
      self.entries.append(entry)
      i += 1
    return self.entries[0]

  def validate(self):
    for entry in self.entries:
      if entry.get().strip() == "":
        tkMessageBox.showwarning("Missing Data",
                                 "You must provide a value for every field.")
        return False
    return True

  def apply(self):
    self.settings.set('ed_companion', 'username', self.entries[0].get().strip())
    self.settings.set('ed_companion', 'password', self.entries[1].get().strip())
    self.settings.set('inara', 'username', self.entries[2].get().strip())
    self.settings.set('inara', 'password', self.entries[3].get().strip())
