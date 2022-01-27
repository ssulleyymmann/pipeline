
pipeline {

    agent none
    stages {
        stage('Build') {

            steps {
sh 'ls'
sh 'pwd'
sh 'docker build  -t vfAnalytics -f $WORKSPACE/Dockerfile .'
            }
        }


    }
}
