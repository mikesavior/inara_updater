#!/usr/bin/python

import actions
import argparse
import gui
import Tkinter as tk
import utils

arg_parser = argparse.ArgumentParser()
arg_parser.add_argument("--no-gui",
                        help="Just update and report to the command line.",
                        action="store_false", dest="gui")

def _settings_prompt_cli(settings):
  settings.set('ed_companion', 'username', raw_input("Elite Username (email address): "))
  settings.set('ed_companion', 'password', raw_input("Elite Password: "))
  settings.set('inara', 'username', raw_input("Inara Username: "))
  settings.set('inara', 'password', raw_input("Inara Password: "))
  print "To change these settings later, edit " + filename

def main():
  args = arg_parser.parse_args()

  if args.gui:
    root = tk.Tk()
    root.wm_title("Inara Updater")
    settings = utils.get_settings()
    app = gui.UpdateWindow(root, settings)
    root.minsize(200, 100)
    root.mainloop()

  else:
    settings = utils.get_settings()
    if settings is None:
      util.update_settings(_settings_prompt_cli, settings)
    inara_session = actions.do_logins(settings)
    actions.update_inara(inara_session)
    print("Inara updated!")

if __name__ == '__main__':
  main()
