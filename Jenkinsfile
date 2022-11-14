pipeline {
    agent any

    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'sudo docker build -t test-randomthought:v1 .'
            }
        }
    }
}