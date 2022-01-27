pipeline {

    agent none
    stages {
        stage('Build images')
        {
            steps {
                      echo "workspace directory is ${workspace}"
                      sh 'ls'
                      sh 'pwd'
                       sh 'docker build  -t vfAnalytics -f $WORKSPACE/Dockerfile .'
            }
   
           
        }
    }
}

