pipeline {
    agent any
    environment {
        dockerhub=credentials('DockerHub')
    }
    stages {
        stage('Clone Repository') {
            steps {
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build .'
            }
        }
        stage('Publish to DockerHub') {
            steps {
                sh 'echo $dockerhub_PSW | docker login -u $dockerhub_USR --password-stdin'

                sh 'docker push al3xfreeman/randomthought:latest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'docker-compose up -d'
            }
        }
        
    }
}