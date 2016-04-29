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

import os, sys, argparse, json
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import loginmanager

#A small utility to quickly add/edit/delete urls to the enviroment
#Examples:
#   Add: python vault-user.py -action add -a bodgeit -e production -u bob -p password -r student
#   Edit: python vault-user.py -action edit -a bodgeit -e production -u bob -p newpass -r student
#   Delete: python vault-user.py -action del -a bodgeit -e production -u bob
#   Dump: python vault-user.py -action dump

def main(argv):
    parser = argparse.ArgumentParser(description="Add/Update/Delete a URL in the URL manager")
    parser.add_argument("-action", type=str, required=True, help="add (create URL), del(delete URL), edit(edit URL), dump (display URL contents)")
    parser.add_argument("-a", type=str, help="application name")
    parser.add_argument("-e", type=str, help="environment")
    parser.add_argument("-u", type=str, help="URL")

    args = parser.parse_args()
    choice = args.action
    if choice == "dump":
        data = loginmanager.openSettingsFile(loginmanager.urlsFile)
        print json.dumps(data, sort_keys=True, indent=4)
    elif choice == "add":
        if args.a is not None and args.e is not None and args.u is not None:
            data = loginmanager.openSettingsFile(loginmanager.urlsFile)
            loginmanager.createURL(data, args.a, args.e, args.u)
            loginmanager.saveSettingsFile(loginmanager.urlsFile, data)
            print "URL: " + args.u + " added"
        else:
            print "Please enter all the arguments for creating a new url:\n -a (app), -e (environment), -u (URL)"
    elif choice == "edit":
        if args.a is not None and args.e is not None and args.u is not None:
            data = loginmanager.openSettingsFile(loginmanager.urlsFile)
            loginmanager.updateURL(data, args.a, args.e, args.u)
            loginmanager.saveSettingsFile(loginmanager.urlsFile, data)
            print "URL: " + args.u + " updated"
        else:
            print "Please enter all the arguments for editing a new url:\n -a (app), -e (environment), -u (URL)"
    elif choice == "del":
        if args.a is not None and args.e is not None and args.u:
            data = loginmanager.openSettingsFile(loginmanager.urlsFile)
            loginmanager.delURL(data, args.a, args.e, args.u)
            loginmanager.saveSettingsFile(loginmanager.urlsFile, data)
            print "URL: " + args.u + " updated"
        else:
            print "Please enter all the arguments for deleting a new url:\n -a (app), -e (environment), -u (URL)"

if __name__ == "__main__":
   main(sys.argv[1:])
