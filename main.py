#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import webapp2
import cgi
import re


USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return PASS_RE.match(password)

EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")
def valid_email(email):
    return EMAIL_RE.match(email)

header = "<h2>Sign Up</h2>"

Ulabel = "<label>Username &emsp;&emsp;&ensp; </label>"
Uinput = "<input type='text' name='username' value='%(username)s'>"

Plabel = "<label>Password &emsp;&emsp;&ensp;&nbsp; </label>"
Pinput = "<input type='password' name='password'>"

Vlabel = "<label>Verify Password &nbsp;</label>"
Vinput = "<input type='password' name='verify'>"

Elabel = "<label>Email &emsp;&emsp;&emsp;&emsp;&nbsp; </label>"
Einput = "<input type='text' name='email' value='%(email)s'>"

submit = "<input type='submit'/>"
form = "<form method='post'>" + Ulabel + Uinput + "%(Uerror)s<br>" + Plabel + Pinput + "%(Perror)s<br>" + Vlabel + Vinput + "%(Verror)s<br>" + Elabel + Einput + "%(Eerror)s<br>" + submit + "<br></form>"

content = header + form


class WelcomeHandler(webapp2.RequestHandler):

    def get(self):
        username = self.request.get("username")
        self.response.out.write("Welcome, " + username + "!")


class MainHandler(webapp2.RequestHandler):

    def build_page(self, Uerror='', Perror='', Verror='', Eerror='', username='', email=''):
        self.response.write(content %{"Uerror":Uerror, "Perror":Perror, "Verror":Verror, "Eerror":Eerror,"username":username, "email":email})


    def get(self):
        self.build_page('','','','','','')

    def post(self):
        username = self.request.get("username")
        password = self.request.get("password")
        verify = self.request.get("verify")
        email = self.request.get("email")

        Usend = ""
        Psend = ""
        Vsend = ""
        Esend = ""
        error = False

        if not valid_username(username):
            Usend = "That's not a valid username."
            error = True

        if not valid_password(password):
            Psend = "That wasn't a valid password."
            error = True

        if verify != password:
            Vsend = "Your password's didn't match."
            error = True

        if not valid_email(email) and email != (""):
            Esend = "That's not a valid email."
            error = True

        if error:
            self.build_page(Usend, Psend, Vsend, Esend, username, email)
        else:
            self.redirect("/welcome?username=" + username)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/welcome', WelcomeHandler)
], debug=True)
