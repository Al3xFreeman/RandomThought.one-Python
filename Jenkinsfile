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
                sh 'docker build -t test-randomthought:v1 .'
            }
        }
        stage('Run Image') {
            steps {
                sh 'docker run --rm test-randomthought:v1'
            }
        }
    }
}