##JuaKali a security automation and retesting utility
JuaKali allows for security retesting using Jenkins and security testing frameworks such as Guantlt. The name come from the swahili word, JuaKali, which is given to craftsmen who work in the hot sun making products with materials they have at hand. This utility is simply using what many organization have on hand to build simple security tests.

##Install
**Cloning**

    git clone https://github.com/aaronweaver/JuaKali.git

Install the git plugin for Jenkins, or your preferred SCM plugin and the Slack plugin. Alternatively you can use the hipchat plugin.

**Setup**

    $ sh setup.sh

Create your first security test::

    $ cd scripts/bin
    $ ./set-env.sh
    $ python create-job.py -test curl -folder defects -name "XSS on Bodgeit Login"
    $ jenkins-jobs --conf $JUAKALIINSTALL/config/env/jenkins_job.ini update -r $JUAKALIINSTALL/job-templates/jenkins-master-templates:$JUAKALIINSTALL/security-tests

##Folder setup
* All security tests are in security-tests/defects or security-tests/health-checks
* In each folder is the yaml file which is used for loading tests into Jenkins. For the most part you will not need to edit this file. The other file in the folder is the .attack file which is a Guantlt script. Edit this script for your particular security test.
* The master templates for the Jenkins jobs are in job-templates/jenkins-master-templates. The majority of customization will be done by editing these two files.


     `$ jenkins-jobs --conf $JUAKALIINSTALL/config/env/jenkins_job.ini update -r job-templates/jenkins-master-templates/master-security-tests-jenkins.yaml`

##Master Job
There is a master template job that can be used to create a job that pulls in the latest security tests and automatically builds them in Jenkins. This file is in job-templates/master-job-config/master-security-test-jenkins.yaml. Edit this file adding your particular configuration and then run the Jenkins builder job.

##Build Script
In scripts/bin there is a build.sh file that will checkin the code and kick off your Jenkins job. The script will also verify that the yaml files are correct before committing the files.
  $ build.sh "Created an XSS test for Bodgeit"

##Version Note
The pip install of Jenkins Builder doesn't seem to have slack support yet. If that's the case then do a git pull from source as that has Slack support.

**Cloning**

    git clone https://git.openstack.org/openstack-infra/jenkins-job-builder

##Dependencies

###Jenkins
* The example configuration files use the git and slack plugins. Install these before running Jenkins Builder
* Ruby requires a little special treatment to run on Jenkins, this article does a decent job in describing how to go about doing that. https://rvm.io/integration/jenkins
* Modify Jenkin's login user profile and add the variable for where JuaKali is installed: $JUAKALIINSTALL=/path/to/install
* There is a bug in certain versions of Jenkins that require a Jenkins restart. If you get an error when running Jenkins builder that outputs a slack error, then restart the server.

###Install Gauntlt
https://github.com/gauntlt/gauntlt

###Utilizes Jenkins Job Builder to create security tests in Jenkins
http://docs.openstack.org/infra/jenkins-job-builder/index.html

###Ansible Vault
https://pypi.python.org/pypi/ansible-vault/1.0.3
