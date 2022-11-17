pipeline {
    agent any
    environment {
        dockerhub=credentials('DockerHub')
        remote='alex@192.168.1.67'
        git_repo=credentials('randomthought_repo')
        loc='Documents/randomThought/app_data/RandomThought.one-Python'
        direct_ssh='ssh alex@192.168.1.67 "cd Documents/randomThought/app_data/RandomThought.one-Python ; '
    }
    stages {
        stage('Checkout') {
            steps {
                checkout scm
                sh 'echo EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE'
                echo "${env.BUILD_ID}"

            }
        }
        stage('Clone Repository in remote server') {
            steps {
                sh 'ssh $remote "cd $loc ; git pull $git_repo"'
            }
        }
        stage('Build Image') {
            steps {
                sh "ssh $remote \"cd $loc ; docker build -t al3xfreeman/randomthought:latest -t al3xfreeman/randomthought:\\\"${env.BUILD_ID}\\\" . \""
            }
        }
        stage('Publish to DockerHub') {
            steps {
                sh "ssh $remote \"cd $loc ; echo $dockerhub_PSW | docker login -u $dockerhub_USR --password-stdin \""

                sh "ssh $remote \"cd $loc ; docker push al3xfreeman/randomthought:\\\"${env.BUILD_ID}\\\" \""
                sh "ssh $remote \"cd $loc ; docker push al3xfreeman/randomthought:latest" \""
            }
        }
        stage('Deploy') {
            steps {
                sh 'ssh $remote "cd $loc ; ls "'
                sh 'ssh $remote "cd $loc ; docker-compose pull "'
                sh 'ssh $remote "cd $loc ; docker-compose up -d "'
            }
        }
    }
}