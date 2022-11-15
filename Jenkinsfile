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
                sh 'docker build -t randomthought:latest .'
            }
        }
        stage('Publish to DockerHub') {
            steps {
                sh 'docker tag randomthought:latest al3xfreeman/randomthought:latest'
                sh 'echo $dockerhub_PSW | docker login -u $dockerhub_USR --password-stdin'

                sh 'docker push randomthought:latest .'
            }
        }
        
    }
}