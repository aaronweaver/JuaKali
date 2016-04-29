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

import os, sys, json, argparse, uuid, random, string
import jinja2
from argparse import RawTextHelpFormatter
from shutil import copyfile
from jinja2 import Template

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import loginmanager

#Whitelist the acceptable characters
def formatFileName(filename):
    valid_chars = "-_() %s%s" % (string.ascii_letters, string.digits)
    filename = ''.join(c for c in filename if c in valid_chars)

    #Remove any spaces or underscores in the name
    filename = filename.replace("-","_")
    filename = filename.replace(" ","_")

    return filename

#Replaces the tags in the the templates
def processTemplate(templateSource, templateVars, destination):
    #Setup jinja2 for creating the template
    templateLoader = jinja2.FileSystemLoader( searchpath="/" )
    templateEnv = jinja2.Environment( loader=templateLoader )
    template = templateEnv.get_template(templateSource)

    #Process the template to produce the final text.
    outputText = template.render( templateVars )
    file = open(destination, "w")
    file.write(outputText)
    file.close()

def setupProject(templateType, targetFolder, projectName, testid):
    #Make sure the filename is valid
    projectName = formatFileName(projectName)

    #format testid
    testid = formatFileName(testid)

    #Set the path to the destination project directory
    testDirectory = os.path.join(os.path.dirname(__file__), "../../security-tests/")
    #Set the path to the template directory
    baseTemplateDir = os.path.realpath(os.path.join(os.path.dirname(__file__), "../../job-templates/"))

    #Determine which tempalte to create
    if templateType == "curl":
        gauntltTemplate = "generic-curl.attack"
        destGauntltTemplate = "curl.attack"
    elif templateType == "nmap":
        gauntltTemplate = "nmap.attack"
        destGauntltTemplate = "nmap.attack"
    elif templateType == "generic":
        gauntltTemplate = "generic.attack"
        destGauntltTemplate = "generic.attack"
    elif templateType == "auth":
        gauntltTemplate = "auth.attack"
        destGauntltTemplate = "auth.attack"
    else:
        print "That template option is not available: " + templateType
        return

    #Determine the target directory for copying the test files into and
    #the appropriate Jenkins YAML file
    if targetFolder == "defects":
        targetFolder = "defects"
        yamlFile = "jenkins-generic.yaml"
    elif targetFolder == "health-checks":
        targetFolder = "health-checks"
        yamlFile = "health-check.yaml"
    elif targetFolder == "scans":
        targetFolder = "scans"
        yamlFile = "jenkins-generic.yaml" #Review and check if this yaml file needs to be customized
    else:
        return "Target directory not defined. Choices are: defects, health-checks or scans"

    #Create the project directory in the security-tests folder
    if not os.path.exists(os.path.realpath(testDirectory + targetFolder)) :
        os.mkdir(os.path.realpath(testDirectory + targetFolder))

    friendlyName = projectName
    if testid is None:
        #Generate a unique id so that jobs can be referenced by a number
        random.seed(os.urandom(10))
        jobid = str(random.randrange(1, 99999)).zfill(5)
    else:
        jobid = testid
    projectName = projectName + "_" + jobid

    #Set the path to the destination project directory
    projectDirectory = os.path.join(os.path.dirname(__file__), "../../security-tests/" + targetFolder + "/" + projectName)

    #Create the project directory
    if not os.path.exists(projectDirectory):
        os.mkdir(projectDirectory)

    #Values for the jobs template
    templateVars = { "jenkinsProjectName" : "project-" + str(uuid.uuid1()),
                   "folder" : targetFolder + "/" + projectName,
                   "jenkinsJobName" : friendlyName,
                   "jobid" : jobid
                   }
    templateSource = baseTemplateDir + "/security-templates/yaml/" + yamlFile
    processTemplate(templateSource, templateVars, os.path.join(projectDirectory + "/" + projectName + ".yaml"))

    #Copy the template inot the destination directory
    sourceFile = os.path.realpath(os.path.join(baseTemplateDir + "/security-templates/attack/" + gauntltTemplate))
    projectDirectory = os.path.realpath(projectDirectory)

    #Auth is the only template that needs substitute, this may change in the future
    if templateType == "auth":
        #Values for the gauntlt template
        templateVars = { "pythonPath" : "security-tests/" + targetFolder + "/" + projectName + "/auth.py" }
        templateSource = baseTemplateDir + "/security-templates/attack/" + destGauntltTemplate
        processTemplate(templateSource, templateVars, os.path.join(projectDirectory + "/" + destGauntltTemplate))
    else:
        #Copy the template inot the destination directory
        copyfile(sourceFile, projectDirectory + "/" + destGauntltTemplate)

    #Copy the python file
    if templateType == "auth":
        #Copy the python file into the destination project folder
        sourceFile = os.path.realpath(os.path.join(baseTemplateDir + "/security-templates/attack/auth.py"))
        projectDirectory = os.path.realpath(projectDirectory)
        #Copy the template inot the destination directory
        copyfile(sourceFile, projectDirectory + "/auth.py")

    returnTxt = "\n\n###################################################\n"
    returnTxt = returnTxt + "Created project: " + projectName + "\n"
    returnTxt = returnTxt + "Folder: " + projectDirectory + "\n"
    returnTxt = returnTxt + "Edit the attack file: " + projectName + ".yaml" + "\n"
    returnTxt = returnTxt + "Run the Gauntlt comand below to verify your test works as expected" + "\n"
    returnTxt = returnTxt + "$GAUNTLT/gauntlt '" + projectDirectory + "/*.attack'" + "\n"
    returnTxt = returnTxt + "###################################################" + "\n\n"
    return returnTxt

#A small utility to aide in creating a new jenkins security job
def main(argv):
    parser = argparse.ArgumentParser(description=
    """
    Creates security templates for Jenkins:
    Examples:
       nmap Test: python create-job.py -test nmap -folder health-checks -name "Monitor Bodgeit Site HTTP and HTTPS"
       Curl Test: python create-job.py -test curl -folder defects -name "XSS on Bodgeit Login"
       Auth Test: python create-job.py -test auth -folder defects -name "XSS in Admin Report"
    """,
    formatter_class=RawTextHelpFormatter)
    parser.add_argument("-test", type=str, required=True, help="Choice: auth, generic, nmap or curl")
    parser.add_argument("-folder", type=str, required=True, help="Target folder: (Choice: defect, health-checks or scans)")
    parser.add_argument("-name", type=str, required=True, help="Name of the security test")
    parser.add_argument("-testid", type=str, required=False, help="ID for the test, can relate to a DefectDojo or Jira Number")

    #Parse command line arguements
    args = parser.parse_args()

    #### Creates the project folder along with the gauntl and yaml files needed to create the jenkins job
    print setupProject(args.test, args.folder, args.name, args.testid)

if __name__ == "__main__":
   main(sys.argv[1:])
