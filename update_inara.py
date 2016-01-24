#!/usr/bin/python

import argparse
from datetime import datetime
from elite_api import companion
from elite_api.inara import InaraSession
import Tkinter as tk
import utils

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--no-gui",
                        help="Just update and report to the command line.",
                        action="store_false", dest="gui")


def do_logins(settings):
  inara_session = InaraSession(settings.get('inara', 'username'), settings.get('inara', 'password'))
  companion.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
  return inara_session


def update_inara(inara_session):
  data = companion.get_data()
  inara_session.update_credits(data['commander']['credits'])
  inara_session.update_location(data['lastSystem']['name'])


class UpdateWindow(object):
  def __init__(self, parent, settings):
    self.parent = parent
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
                              command=lambda: utils.update_settings(True, parent, settings))
    config_button.grid(row=1, column=1, sticky=tk.E+tk.S, padx=5, pady=5)

    try:
      self.session = do_logins(settings)
    except:
      self.update_button['state'] = tk.DISABLED
      self.message.set("Error logging in. Double-check your config,\nthen restart the program.")

  def _update_inara(self):
    self.message.set("Updating, please wait...")
    self.parent.update()
    update_inara(self.session)
    self.message.set("Update successful! (Last update: %s)" %
                     datetime.now().isoformat(' ')[:16])


def main():
  args = arg_parser.parse_args()

  if args.gui:
    root = tk.Tk()
    root.wm_title("Inara Updater")
    settings = utils.get_settings(True, root)
    app = UpdateWindow(root, settings)
    root.mainloop()
  else:
    settings = utils.get_settings(False)
    inara_session = do_logins(settings)
    update_inara(inara_session)
    print("Inara updated!")

if __name__ == '__main__':
  main()
