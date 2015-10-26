#!/usr/bin/python

from companion import Session, VerificationRequired
import os
import utils

def main():
  settings = utils.get_settings()
  session = Session()

  try:
    session.login(settings.get('ed_companion', 'username'), settings.get('ed_companion', 'password'))
  except VerificationRequired:
    code = raw_input("Input Verification Code: ")
    session.verify(code)

  data = session.query()

  # Now we have the data!
  print "Commander %s" % data['commander']['name']
  print "Credits: %s" % data['commander']['credits']
  print "Location: %s" % data['lastSystem']['name']
  
  session.close()

if __name__ == "__main__":
  main()
