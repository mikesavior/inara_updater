#!/usr/bin/python

from companion import Session, VerificationRequired
import argparse
import os
import utils

flag_parser = argparse.ArgumentParser(description="Report information about your Elite: Dangerous character.")
flag_parser.add_argument('--dump', action='store_true', help="Dump raw data.")

def main():
  settings = utils.get_settings()
  session = Session()
  flags = flag_parser.parse_args()

  try:
    session.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
  except VerificationRequired:
    code = raw_input("Input Verification Code: ")
    session.verify(code)

  data = session.query()

  # Now we have the data!
  if flags.dump:
    print data
  else:
    print "Commander %s" % data['commander']['name']
    print "Credits: %s" % data['commander']['credits']
    print "Location: %s" % data['lastSystem']['name']
  
  session.close()

if __name__ == "__main__":
  main()
