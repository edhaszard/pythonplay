import sys
import requests
import os
import pyad
import win32

from pyad import *
pyad.set_defaults(ldap_server="prd-ad-02.ihc.co.nz")
pyad.
userMe = adsearch.by_upn ("ed.haszard@ihc.org.nz")

userMeCN = pyad.aduser.ADUser.from_cn("Ed Haszard Morris")

#userMe.set_attribute("description", "here's a python description")


print(userMeCN)

ou = pyad.adcontainer.ADContainer.from_dn("ou=testing,ou=it,ou=user accounts,dc=ihc,dc=co,dc=nz")

new_group = pyad.adgroup.ADGroup.from_cn("Test Group 123456789")

new_group.move(pyad.adcontainer.ADContainer.from_dn("ou=testing,ou=it,ou=user accounts,dc=ihc,dc=co,dc=nz"))