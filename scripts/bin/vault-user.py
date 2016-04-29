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

import os, sys, json, argparse
from argparse import RawTextHelpFormatter
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import loginmanager

#A small utility to quickly add/edit/delete a user from the vault database
#Examples:
#   Add: python vault-user.py -action add -a bodgeit -e production -u bob -p password -r student
#   Edit: python vault-user.py -action edit -a bodgeit -e production -u bob -p newpass -r student
#   Delete: python vault-user.py -action del -a bodgeit -e production -u bob
#   Dump: python vault-user.py -action dump

def main(argv):
    parser = argparse.ArgumentParser(description=
    """
    Add/Update/Delete a user in the password vault
    Examples:
       Add: python vault-user.py -action add -a bodgeit -e production -u bob -p password -r student
       Edit: python vault-user.py -action edit -a bodgeit -e production -u bob -p newpass -r student
       Delete: python vault-user.py -action del -a bodgeit -e production -u bob
       Dump: python vault-user.py -action dump""",
    formatter_class=RawTextHelpFormatter)
    parser.add_argument("-action", type=str, required=True, help="add (create new user), del(delete user), edit(edit user), dump (display vault contents)")
    parser.add_argument("-a", type=str, help="application name")
    parser.add_argument("-e", type=str, help="environment")
    parser.add_argument("-u", type=str, help="user")
    parser.add_argument("-p", type=str, help="password")
    parser.add_argument("-r", type=str, help="role")

    args = parser.parse_args()
    choice = args.action
    if choice == "dump":
        data = loginmanager.openVaultFile(loginmanager.vaultFile)
        print json.dumps(data, sort_keys=True, indent=4)
    elif choice == "add":
        if args.a is not None and args.e is not None and args.u is not None and args.p is not None and args.r is not None:
            data = loginmanager.openVaultFile(loginmanager.vaultFile)
            loginmanager.addUser(data, args.a, args.e, args.u, args.p, args.r)
            loginmanager.saveVaultFile(loginmanager.vaultFile, data)
            print "User: " + args.u + " added"
        else:
            print "Please enter all the arguments for creating a new user:\n -a (app), -e (environment), -u (user), -p (password) and -r (role)"
    elif choice == "edit":
        if args.a is not None and args.e is not None and args.u is not None and args.p is not None and args.r is not None:
            data = loginmanager.openVaultFile(loginmanager.vaultFile)
            loginmanager.addUser(data, args.a, args.e, args.u, args.p, args.r)
            loginmanager.saveVaultFile(loginmanager.vaultFile, data)
            print "User: " + args.u + " updated"
        else:
            print "Please enter all the arguments for editing a user:\n -a (app), -e (environment), -u (user), -p (password)"
    elif choice == "del":
        if args.a is not None and args.e is not None and args.u:
            data = loginmanager.openVaultFile(loginmanager.vaultFile)
            loginmanager.delUser(data, args.a, args.e, args.u)
            loginmanager.saveVaultFile(loginmanager.vaultFile, data)
            print "User: " + args.u + " updated"
        else:
            print "Please enter all the arguments for deleting a user:\n -a (app), -e (environment), -u (user), -p (password)"

if __name__ == "__main__":
   main(sys.argv[1:])
