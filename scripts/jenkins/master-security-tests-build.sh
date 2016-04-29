#copy the git scripts and yaml files into the jenkins home directory
#Check to make sure the $workspace variable is set
if [ -z "$WORKSPACE" ]
then
  echo "Jenkins WORKSPACE is not set, file copy will not take place."
else
  echo "Copying files from workspace to local folder"
  #echo rsync -avz --exclude 'config/env/' --exclude '.git' --exclude 'venv/' $WORKSPACE/ $JUAKALIINSTALL
  #rsync -avz --exclude 'config/env/' --exclude '.git' --exclude 'venv/' $WORKSPACE/ $JUAKALIINSTALL
  rsync -rv --delete  --exclude='config/env/' --exclude='.git' --exclude='venv/' /var/lib/jenkins/jobs/Master-Security-Tests-Build/workspace/ $JUAKALIINSTALL/
fi

if [ -z "$JUAKALIINSTALL" ]
then
  echo "Jenkins security automation path not set, please define in scripts/bin/set-env.sh"
  exit 1
fi

#cd $JUAKALIINSTALL
echo
##############################
#Slack support not in current pip install
#Change this once that's done
#For now git clone from https://github.com/openstack-infra/jenkins-job-builder/
##############################
echo "Activating the virtual environment"
. /opt/jenkins-job-builder/venv/bin/activate
echo
echo
echo "Running Jenkins-Job-Builder"
jenkins-jobs --conf $JUAKALIINSTALL/config/env/jenkins_job.ini update -r $JUAKALIINSTALL/job-templates/jenkins-master-templates:$JUAKALIINSTALL/security-tests
