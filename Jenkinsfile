
pipeline {

    agent any
    stages {
        stage('Build') {

            steps {
sh 'ls'
sh 'pwd'
sh 'docker build  -t vfanalytics -f $WORKSPACE/Dockerfile .'
            }
        }


    }
}
