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

from ansible_vault import Vault
import os

#Set the vault password via bash
#export vaultpwd='secret'
vaultpwd = None

if vaultpwd in os.environ:
    vaultpwd = os.environ["vaultpwd"]

vaultFile = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'vault', 'credentials.yaml')

#To edit manually open the file with Ansible `ansible-vault edit credentials.yaml`
#Loads the yaml vault file
def openVaultFile(file):
    vault = Vault(vaultpwd)
    data = vault.load(open(vaultFile).read())
    return data

#Save the yaml vault file
def saveVaultFile(file, data):
    vault = Vault(vaultpwd)
    vault.dump(data, open(vaultFile, 'w'))
    #return data

#Create a user in the yaml vault file
#Format:
#bodgeit:                   #Application Name
#  staging:                 #Environment
#    user-1:                #Username
#      password: secret     #Pasword
#      role: shopper        #Role
def addUser(settings, product, env, username=None, password=None, role=None):
    #If the product doesn't exist then create it
    if not product in settings:
        settings[product] = {}

    #If the environment doesn't exist then create it
    prodData = settings[product]
    if not env in prodData:
            settings[product][env] = {}

    #If the username doesn't exist then create it
    envData = settings[product][env]
    if not username in envData:
        settings[product][env][username] = {} #Create the object

    #Set the role
    settings[product][env][username]["role"] = role
    #Set the password
    settings[product][env][username]['password'] = password

#Update password or role in the yaml vault file
#Format:
#bodgeit:                   #Application Name
#  staging:                 #Environment
#    user-1:                #Username
#      password: secret     #Pasword
#      role: shopper        #Role
def editEntry(settings, product, env, username, password=None, role=None):
    if password is not None:
        settings[product][env][username]['password'] = password

    if role is not None:
        settings[product][env][username]['role'] = role

#Returns an object with the username, role and password
def getCreds(product, env, username):
    data = openVaultFile(file)
    return data[product][env][username]

def delProduct(settings, product):
    del(settings[product])

def delEnv(settings, product, env):
    del(settings[product][env])

def delUser(settings, product, env, username):
    del(settings[product][env][username])

def dumpVault(settings):
    return settings
