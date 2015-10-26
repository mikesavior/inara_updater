# This class exists to satisfy dependencies in companion.py.
# It's mostly a stub; I don't want to pull EDMC's config.py
# without first understanding more of its semantics.
# For username/password settings, see Readme.md

from os import path
import os

class Config():
  app_dir = path.join(path.expanduser('~'), '.ed_tool/')

  def __init__(self):
    try:
      os.mkdir(self.app_dir)
    except OSError:
      pass # Ignore existing directory
      

config = Config()
