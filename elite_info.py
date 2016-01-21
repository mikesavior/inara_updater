#!/usr/bin/python

from elite_api import companion
import argparse
from pprint import pprint
import os
import utils

flag_parser = argparse.ArgumentParser(description="Report information about your Elite: Dangerous character.")
flag_parser.add_argument('--dump', action='store_true', help="Dump raw data.")

def main():
  settings = utils.get_settings()
  session = Session()
  flags = flag_parser.parse_args()

  companion.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
  data = companion.get_data()

  # Now we have the data!
  if flags.dump:
    pprint(data)
  else:
    print "Commander %s" % data['commander']['name']
    print "Credits: %s" % data['commander']['credits']
    print "Location: %s" % data['lastSystem']['name']
  
  session.close()

if __name__ == "__main__":
  main()
