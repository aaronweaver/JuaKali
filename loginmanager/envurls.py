##################################################################
# Program written by Aaron Weaver <aaron.weaver@owasp.org>
# as part of the OWASP AppSec Pipeline project:
# https://www.owasp.org/index.php/OWASP_AppSec_Pipeline
#
# JuaKali is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
##################################################################

import yaml
import os

urlsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'urls', 'urls.yaml')

#To edit the file via Ansible ansible-vault edit credentials.yaml
#Loads the yaml settings file
def openSettingsFile(file):
    with open(file, 'r') as ymlfile:
        data = yaml.load(ymlfile)
    return data

#Save the yaml settings file
def saveSettingsFile(file, data):
    with open(file, 'w') as ymlfile:
        ymlfile.write( yaml.dump(data, default_flow_style=False) )

#Create an environment and URL in the yaml file
#Example Format:
#bodgeit:
#  new-value: http://localhost/login
def createURL(settings, product, env, url):
    if product in settings:
        settings[product][env] = url
    else:
        settings[product] = {}
    settings[product][env] = url

#Update a URL given the product and environment
def updateURL(settings, product, env, url):
    settings[product][env] = url

#Delete and enviornment give the environment and URL
def delURL(settings, product, env, url):
    del settings[product][env]

#Delete a product given the product
def delProd(settings, product):
    if product in settings:
        del settings[product]

#List the contents of the file
def dumpSettings(settings):
    print settings
