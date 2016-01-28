import actions
from datetime import datetime
import Tkinter as tk
import tkSimpleDialog, tkMessageBox
import utils

class UpdateWindow(object):
  def __init__(self, parent, settings):
    self.parent = parent
    if settings is not None:
      self.settings = settings
    else:
      self.settings = utils.update_settings(self._render_config_dialog, self.settings)
    self.frame = tk.Frame(parent)
    self.frame.pack(expand=True, fill=tk.BOTH)

    self.message = tk.StringVar()
    self.message.set("Click Update to update!")
    message_label = tk.Label(self.frame, textvariable=self.message)
    message_label.grid(columnspan=2, padx=20, pady=20)

    self.update_button = tk.Button(self.frame, text="Update", height=2, width=4,
                                   command=self._update_inara)
    self.update_button.grid(row=1, column=0, pady=10)

    config_button = tk.Button(self.frame, text="Config", height=1, width=2,
                              command=self._update_settings)
    config_button.grid(row=1, column=1, sticky=tk.E+tk.S, padx=5, pady=5)

    self._try_login()

  def _update_inara(self, second_try=False):
    self.message.set("Updating, please wait...")
    self.parent.update()
    try:
      actions.update_inara(self.session)
      self.message.set("Update successful! (Last update: %s)" %
                       datetime.now().isoformat(' ')[:16])
    except:
      if second_try:
        self.message.set("Error updating! Double-check your config,\nor try again later.")
      else:
        # We don't use self._try_login() here because we don't want to disable the update button in this case.
        self.session = actions.do_logins(self.settings)
        self._update_inara(True)

  def _update_settings(self):
    self.settings = utils.update_settings(self._render_config_dialog, self.settings)
    self._try_login()

  def _try_login(self):
    try:
      self.session = actions.do_logins(self.settings)
      self.update_button['state'] = tk.NORMAL
    except:
      self.update_button['state'] = tk.DISABLED
      self.message.set("Error logging in. Double-check your config!")

  def _render_config_dialog(self, settings):
    dialog = ConfigDialog(self.frame, settings)


class ShipFrame(tk.Frame):
  INSURANCE = {'0': .05, '1': .04, '2': .02}
  
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)
    self.ship_data = []
    name_header = tk.Label(self, text="Ship Name")
    name_header.grid()
    rebuy_header = tk.Label(self, text="Rebuy")
    name_header.grid(column=1)
    value_header = tk.Label(self, text="Value")
    name_header.grid(column=2)

  def add_ship(self, data):
    """
    'data' should contain the following keys: name, id, rebuy, insurance, date, main, star, description, config, image.
    Some of these are probably blank, but we need to propagate all of them to the Inara form eventually.
    """
    if not self._validate_data(data):
      return False
    label = tk.Label(self, text="%s:" % data['name'])
    label.grid()
    entry = tk.Entry(self, text=value)
    entry.grid(column=1)

    ship_value = int(data['rebuy']) / INSURANCE[data['insurance']]
    value_label = tk.Label(self, text=str(ship_value))
    value_label.grid(column=2)

    data['rebuy_entry'] = entry
    self.ship_data.append(data)

  def _validate_date(self, data):
    return all(key in data.keys() for key in
               ('name', 'id', 'rebuy', 'insurance', 'date', 'main', 'star', 'description', 'config', 'image'))
      


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
