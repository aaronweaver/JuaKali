#!/usr/bin/env bash
echo "=============================================================================="
echo "Welcome to JuaKali! This is a quick script to get you up and running."
echo
echo "Requirements:"
echo "    You'll need the URL to your Jenkins sever, username and password"
echo "    Install Gauntlt and the path to Gauntlt"
echo "=============================================================================="
echo

#Create the config/env files for environment specific configuration
if [[ ! -e config/env ]]; then
    echo "creating directory"
    mkdir config/env
fi

#Copy the jenkins configuration file
cp config/template/jenkins_job.ini.template config/env/jenkins_job.ini

unset HISTFILE

read -p "Setting up Jenkins? Not necessary for a local install (y/n): " JENKINS
if [ $JENKINS == 'y' ]
then
  read -p "Jenkins Server: (http://jenkins-server:8080): " JENKINSSERVER
  echo $JENKINSSERVER
  read -p "Jenkins Username: " JENKINSUSER
  stty -echo
  read -p "Jenkins Password: " JENKINSPASS; echo
  stty echo

  #OSX uses an older version of sed
  if [ "$(uname)" == "Darwin" ]; then
    #Save the settings in the configuration file
    sed -i "" "s~jenkins-server~$JENKINSSERVER~g" config/env/jenkins_job.ini
    sed -i "" "s/jenkins-builder/$JENKINSUSER/g" config/env/jenkins_job.ini
    sed -i "" "s/jenkins-password/$JENKINSPASS/g" config/env/jenkins_job.ini
    sed -i "" "s/jenkins-password/$JENKINSPASS/g" config/env/jenkins_job.ini
  else
    #Save the settings in the configuration file
    sed -i "s~jenkins-server~$JENKINSSERVER~g" config/env/jenkins_job.ini
    sed -i "s/jenkins-builder/$JENKINSUSER/g" config/env/jenkins_job.ini
    sed -i "s/jenkins-password/$JENKINSPASS/g" config/env/jenkins_job.ini
    sed -i "s/jenkins-password/$JENKINSPASS/g" config/env/jenkins_job.ini
  fi
  echo "Jenkins Builder configuration file created in: config/jenkins_job.ini"
  echo
fi

echo "Creating the virtual environment"
#create the virtual environment
virtualenv venv

echo "Activating the virtual environment"
#activate virtual environment
. venv/bin/activate

echo
echo "Installing required packages...."

#install the requirements
pip install -r requirements/requirements.txt

echo
echo "Copying set-env file"
#Copying the set-env file
cp config/template/set-env.sh.template config/env/set-env.sh

echo
echo "Almost complete:"
read -p "Path to Jenkins Security Automation (ex: /opt/jenkins-security-automation): " JENKINSFOLDERPATH
read -p "Path to Gauntlt (ok, to leave blank and add later, ex: /opt/guantlt/): " GAUNTLTFOLDERPATH
read -p "Vault Password (Credential storage for login scripts): " PASSWORD

#OSX uses an older version of sed
if [ "$(uname)" == "Darwin" ]; then
  sed -i "" "s~JUAKALIPATH~$JENKINSFOLDERPATH~g" config/env/set-env.sh
  sed -i "" "s~GAUNTLTPATH~$GAUNTLTFOLDERPATH~g" config/env/set-env.sh
  sed -i "" "s~VLTPASSWORD~$PASSWORD~g" config/env/set-env.sh
else
  sed -i "s~JUAKALIPATH~$JENKINSFOLDERPATH~g" config/env/set-env.sh
  sed -i "s~GAUNTLTPATH~$GAUNTLTFOLDERPATH~g" config/env/set-env.sh
  sed -i "s~VLTPASSWORD~$PASSWORD~g" config/env/set-env.sh
fi
echo
echo "Settings updated in config/env/set-env.sh"
echo
echo "=============================================================================="
echo "Complete!"
echo
echo "=============================================================================="
echo
