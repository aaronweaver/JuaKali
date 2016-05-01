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

import requests, yaml, os

secheadername = "YourCompany-Security-Scanner"
secheadervalue = "Contact security@yourcompany.com"
urlsFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'urls', 'urls.yaml')

#Debug with a local proxy
proxies = {
  'http': 'http://localhost:8080',
  'https': 'https://localhost:8080',
}

#Logs the given user into yoursite
def loginSite(userObj, useProxy=False, url=None, debug=False):
    with open(urlsFile, 'r') as ymlfile:
        urlcfg = yaml.load(ymlfile)

    remoteURL = None
    user = userObj["user"]
    password = userObj["password"]
    env = userObj["env"]

    if url is None:
        remoteURL = urlcfg['bodgeit'][env]

    session = requests.Session()

    #####Login to Applia
    paramsPost = {}
    headers = {}

    if useProxy:
        response = session.post(remoteURL, data=paramsPost, headers=headers, proxies=proxies, verify=False)
    else:
        response = session.post(remoteURL, data=paramsPost, headers=headers, verify=False)

    if debug:
        print "Status code:", response.status_code
        print "Response body:", response.content
    return session
