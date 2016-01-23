#!/usr/bin/python

import argparse
from datetime import datetime
from elite_api import companion
from elite_api.inara import InaraSession
import Tkinter as tk
import utils
import easygui

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


class UpdateWindow:
  def __init__(self, parent, settings):
    frame = tk.Frame(parent)
    frame.pack(expand=True, fill=tk.BOTH)

    self.message = tk.StringVar()
    self.message.set("Click Update to update!")
    message_label = tk.Label(frame, textvariable=self.message)
    message_label.grid(columnspan=3, padx=20, pady=20)

    self.update_button = tk.Button(frame, text="Update", height=2, width=4,
                                   command=self._update_inara)
    self.update_button.grid(row=1, column=0, columnspan=2, pady=10)

    config_button = tk.Button(frame, text="Config", height=1, width=2,
                              command=utils.init_settings)
    config_button.grid(row=1, column=2)

    try:
      self.session = do_logins(settings)
    except:
      self.update_button['state'] = tk.DISABLED
      self.message.set("Error logging in. Double-check your config,\nthen restart the program.")

  def _update_inara(self):
    self.message.set("Updating, please wait...")
    update_inara(self.session)
    self.message.set("Update successful! (Last update: %s)" %
                     datetime.now().isoformat(' ')[:16])


def main():
  args = arg_parser.parse_args()

  settings = utils.get_settings(args.gui)

  if args.gui:
    root = tk.Tk()
    root.wm_title("Inara Updater")
    app = UpdateWindow(root, settings)
    root.mainloop()
  else:
    inara_session = do_logins(settings)
    update_inara(inara_session)
    print("Inara updated!")

if __name__ == '__main__':
  main()
