import actions
from datetime import datetime
import Tkinter as tk
import tkSimpleDialog, tkMessageBox
import utils

class UpdateWindow(object):
  def __init__(self, parent, settings):
    self.ship_id = None
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
    message_label.pack(fill=tk.X)

    self.info = InfoFrame(self.frame)
    self.info.pack(fill=tk.X, expand=True, pady=10)

    button_row = tk.Frame(self.frame)
    button_row.pack()
    self.update_button = tk.Button(button_row, text="Update", command=self._update_inara)
    self.update_button.pack(side=tk.LEFT, expand=True)

    self.ship_button = tk.Button(button_row, text="Name Ship", command=self._update_ship_dialog)
    self.ship_button.pack(side=tk.LEFT)
    self.ship_button['state'] = tk.DISABLED
    
    config_button = tk.Button(button_row, text="Config", command=self._update_settings)
    config_button.pack(side=tk.LEFT)

    self._try_login()

  def _update_inara(self, second_try=False):
    self.message.set("Updating, please wait...")
    self.parent.update()
    try:
      data = actions.update_inara(self.session)
    except:
      if second_try:
        self.message.set("Error updating! Double-check your config,\nor try again later.")
        return
      else:
        # We don't use self._try_login() here because we don't want to disable the update button in this case.
        self.session = actions.do_logins(self.settings)
        self._update_inara(True)

    self.ship_id = data['ship_id']
    ship_name = 'Unknown'
    if self.settings.has_option('ships', str(self.ship_id)):
      ship_name = self.settings.get('ships', str(self.ship_id))
    self.info.update_info(data, ship_name)
    self.message.set("Update successful!\n(Last update: %s)" %
                     datetime.now().isoformat(' ')[:16])
    self.ship_button['state'] = tk.NORMAL # Once we have a current ship ID, we can use the ship button.

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

  def _update_ship_dialog(self):
    dialog = ShipDialog(self.frame, self.settings, self.ship_id)


class InfoFrame(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)

    self.cmdr = self._add_row("CMDR:")
    self.ship = self._add_row("Current Ship:")
    self.system = self._add_row("Location:")
    self.credits = self._add_row("Credit Balance:")
    self.assets = self._add_row("Current Assets:")

  def update_info(self, data, ship_name):
    self.cmdr.set(data['cmdr'])
    self.ship.set(ship_name)
    self.system.set(data['location'])
    self.credits.set(str(data['credits']))
    self.assets.set(str(data['assets']))

  def _add_row(self, label_text):
    row = tk.Frame(self)
    row.pack(expand=True, fill=tk.X)
    label = tk.Label(row, text=label_text)
    label.pack(side=tk.LEFT, anchor=tk.W)
    value = tk.StringVar()
    value_label = tk.Label(row, textvariable=value)
    value_label.pack(side=tk.RIGHT, anchor=tk.E)
    return value


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



class ShipDialog(tkSimpleDialog.Dialog):
  def __init__(self, parent, settings, ship_id, title="Ship Name"):
    self.settings = settings
    self.ship_id = ship_id
    tkSimpleDialog.Dialog.__init__(self, parent, title)
    
  def body(self, parent):
    ship_name = ''
    if self.settings.has_option('ships', str(self.ship_id)):
      ship_name = self.settings.get('ships', str(self.ship_id))
        
    label = tk.Label(parent, text="Enter your ship's name.\nThis should match what is entered in Inara.\n(Note: This feature doesn't do much yet)")
    label.pack()
    self.entry = tk.Entry(parent, width=30)
    self.entry.insert(0, ship_name)
    self.entry.pack()
    return self.entry

  def apply(self):
    utils.settings_update_ship(self.settings, self.ship_id, self.entry.get().strip())
