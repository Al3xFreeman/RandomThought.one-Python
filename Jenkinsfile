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
        stage('Parallel building') {
            parallel {
                stage('AMD64 Build') {
                    steps {
                        sh 'docker buildx create --use --name buildx_adm64'
                        sh 'docker buildx build --platform linux/amd64 -t al3xfreeman/randomthought:latest .'
                    }
                }
                stage('ARM64/V8 Build') {
                    steps {
                        sh 'docker buildx create --use buildx_arm64_v8'
                        sh 'docker buildx build --platform linux/arm/v8 -t al3xfreeman/randomthought:latest .'
                    }
                }
            }
        }
        stage('Publish to DockerHub') {
            steps {
                sh 'echo $dockerhub_PSW | docker login -u $dockerhub_USR --password-stdin'

                sh 'docker push al3xfreeman/randomthought:latest'
            }
        }
        
    }
}