#!/bin/bash
#Creates the master jenkins job
cd /opt/jenkins-job-builder

echo "Activating the virtual environment"
. venv/bin/activate

echo "Running Jenkins-Job-Builder"
jenkins-jobs --conf etc/jenkins_jobs.ini update -r /opt/jenkins-security-automation/job-templates/master-job-config/master-security-tests-jenkins.yaml

echo "Change permissions for the jenkins script folder"
chown -R jenkins:jenkins /opt/jenkins-security-automation
