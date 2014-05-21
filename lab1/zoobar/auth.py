from flask import g
import hashlib
import random

from zoodb import *

class User(object):
    def __init__(self):
        self.person = None

    def checkLogin(self, username, password):
        person = g.persondb.query(Person).get(username)
        if not person:
            return None
        if person.password == hashlib.md5(password + person.salt).hexdigest():
            return self.loginCookie(person)
        else:
            return None

    def addRegistration(self, username, password):
        person = g.persondb.query(Person).get(username)
        if person:
            return None
        newperson = Person()
        newperson.username = username
        newperson.salt = "%04x" % random.randint(0, 0xffff)
        newperson.password = hashlib.md5(password + newperson.salt).hexdigest()
        g.persondb.add(newperson)
        return self.loginCookie(newperson)

    def loginCookie(self, person):
        self.person = person

        person.token = hashlib.md5("%s%.10f" % (person.password, random.random())).hexdigest()
        return "%s#%s" % (person.username, person.token)

    def logout(self):
        self.person = None

    def checkCookie(self, cookie):
        if not cookie:
            return
        (username, token) = cookie.rsplit("#", 1)
        person = g.persondb.query(Person).get(username)
        if person and person.token == token:
            self.person = person
