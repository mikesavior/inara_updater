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

    self.info = InfoFrame(self.frame)
    self.info.grid(columnspan=2)

    self.update_button = tk.Button(self.frame, text="Update", height=2, width=4,
                                   command=self._update_inara)
    self.update_button.grid(row=2, column=0, pady=10)

    config_button = tk.Button(self.frame, text="Config", height=1, width=2,
                              command=self._update_settings)
    config_button.grid(row=2, column=1, sticky=tk.E+tk.S, padx=5, pady=5)

    self._try_login()

  def _update_inara(self, second_try=False):
    self.message.set("Updating, please wait...")
    self.parent.update()
    try:
      data = actions.update_inara(self.session)
      self.info.update_info(data)
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


class InfoFrame(tk.Frame):
  def __init__(self, parent, *args, **kwargs):
    tk.Frame.__init__(self, parent, *args, **kwargs)

    self.cmdr = self._add_row(0, "CMDR:")
    self.system = self._add_row(1, "Location:")
    self.credits = self._add_row(2, "Credit Balance:")
    self.assets = self._add_row(3, "Current Assets:")

  def update_info(self, data):
    self.cmdr.set(data['cmdr'])
    self.system.set(data['location'])
    self.credits.set(str(data['credits']))
    self.assets.set(str(data['assets']))

  def _add_row(self, row, label_text):
    label = tk.Label(self, text=label_text)
    label.grid(row=row, column=0, sticky=tk.W)
    value = tk.StringVar()
    value_label = tk.Label(self, textvariable=value)
    value_label.grid(row=row, column=1, sticky=tk.E)
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
