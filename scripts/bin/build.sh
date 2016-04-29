#!/bin/bash
#############################################################################
#A quick and dirty script for pushing code and kicking off the jenkins job
#Takes one argument for commit message
#############################################################################

#Verify the job yaml files are correct, pipe output from standard error to grep
#(Note: If running locally slack plugin will not be available)
JOB_OK=`jenkins-jobs --conf $JUAKALIINSTALL/config/jenkins_jobs.ini test -r $JUAKALIINSTALL/job-templates/jenkins-master-templates:$JUAKALIINSTALL/security-tests 2>&1 >/dev/null | grep -e "Duplicate entry found in" -e "Failed to find suitable template named" -e "could not found expected" -e "expected <block end>" | wc -l`

if [ $JOB_OK -eq 0 ]
then
  COMMIT="Commit"
  if [ ! -z "$1" ]
  then
      COMMIT=$1
  fi
  git add -A
  git commit -m "$COMMIT"
  git push

  #If you don't want to use a hook to rebuild then uncomment this command to kick of your job.
  #JENKINS-URL='https://jenkins-user:password@yourjenkinsserver/yourbuildtest/build?token=yourbuildtoken'
  #kick off the jenkins job
  #curl -i -s -k  -X 'POST' \
  #    -H 'User-Agent: Mozilla/5.0' -H 'Content-Type: application/x-www-form-urlencoded' \
  #    --data-binary $'json=%7B%7D' \
  #    '$JENKINS-URL'
else
  echo "Jenkins Job Builder Files are not correct please run the command below to view the error. If you don't have slack installed you will get an error. The check only looks for certain items"
  echo "jenkins-jobs --conf $JUAKALIINSTALL/config/jenkins_jobs.ini test -r $JUAKALIINSTALL/job-templates/jenkins-master-templates:$JUAKALIINSTALL/security-tests"
fi
