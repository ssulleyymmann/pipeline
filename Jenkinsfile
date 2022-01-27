
pipeline {

    agent any
    stages {
        stage('Build') {

            steps {
                sh 'ls'
                sh 'pwd'
                sh 'docker build  -t localhost:8088/repository/my-docker/vfanalytics:latest -f Dockerfile .'
                sh 'docker push localhost:8088/repository/my-docker/vfanalytics:latest' 
            }
        }


    }
}
