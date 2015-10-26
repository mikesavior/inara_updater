#!/usr/bin/python
# -*- coding: utf-8 -*-

# Creates connections to inara.cz to retrieve and update player info.

import requests
import sys

URL_BASE = "http://inara.cz/"
URL_LOGIN = URL_BASE
URL_CMDR = URL_BASE + "cmdr/"

class ServerError(Exception):
  pass

class CredentialsError(Exception):
  pass

class Session(requests.Session):
  def __init__(self):
    requests.Session.__init__(self)

    
  def inara_login(self, username, password):
    if (not username or not password):
      raise CredentialsError()

    data = {
      "loginid": username,
      "loginpass": password,
      "formact": "ENT_LOGIN",
      "location": "intro"
    }

    self._inara_handled_request(self.post, URL_LOGIN, data=data)

    
  def inara_update_credits(self, credits):
    data = {
      "location": "cmdr",
      "formact": "USER_CREDITS_SET",
      "playercredits": credits,
      "playercreditsassets": None,
      "oass": 48126920,
    }
    self._inara_handled_request(self.post, URL_CMDR, data=data)

    
  def inara_update_location(self, location):
    data = {
      'formact': 'USER_LOCATION_SET',
      'playercurloc': location
    }
    self._inara_handled_request(self.post, URL_CMDR, data=data)
    

  def _inara_handled_request(self, func, url, data=None):
    r = func(url, data=data)
    r.raise_for_status()

  def _inara_dump(self, r):
    print "Request:"
    print 'Headers\t%s' % r.request.headers
    print 'Data\t%s' % r.request.body
    print ""

    print "Response:"
    print 'Status\t%s'  % r.status_code
    print 'URL\t%s' % r.url
    print 'Headers\t%s' % r.headers
    print 'Logged in? ', "Yes" if "Logout" in r.text else "No"
    print ""
