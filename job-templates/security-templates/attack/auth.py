######################################################################
# This is a sample file for testing with authenticated logins
# ####################################################################

import requests, sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../"))
import loginmanager

######################################################################
#Edit the login credentials for the test
#URL are defined in the loginmanager and can be edited using the
#script in scripts/bin/login-ur.py and vault-user.py
######################################################################
app = "changeme"            #<-- Change to the app name
env = "prod"                #<-- Change to the environment
username = "user-1"         #<-- Change to the username

######################################################################
#Do not edit; Login to the app and return a valid session
######################################################################
cred = loginmanager.getCreds(app, env, username)
cred["user"] = username
cred["env"] = env
session = loginmanager.loginAplia(cred)

######################################################################
#Edit the line below with your paticular security test
#Use the Burp plugin to generate this portion of code
#Install the 'Reissue Request Scripter' in the Bapp Store
######################################################################
paramsGet = {""}
headers = {""}
response = session.get("your-url", params=paramsGet, headers=headers)

print "Response body:", response.content
