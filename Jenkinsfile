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
                sh 'docker build -t test-randomthought:latest .'
            }
        }
        stage('Run Image') {
            steps {
                sh 'docker-compose up -d'
            }
        }
    }
}