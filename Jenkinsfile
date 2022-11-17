pipeline {
    agent any
    environment {
        dockerhub=credentials('DockerHub')
        remote='alex@192.168.1.67'
        git_repo=credentials('randomthought_repo')
        loc='/Documents/randomThought/app_data/RandomThought.one-Python'
        direct_ssh='ssh alex@192.168.1.67 "cd /Documents/randomThought/app_data/RandomThought.one-Python" ; '
    }
    stages {
        stage('Clone Repository in remote server') {
            steps {
                sh 'ssh $remote "cd $loc ; $git_repo pull"'
            }
        }
        stage('Build Image') {
            steps {
                sh 'ssh $remote "cd $loc ; docker build -t al3xfreeman/randomthought:latest ."'
            }
        }
        stage('Publish to DockerHub') {
            steps {
                sh 'direct_ssh echo $dockerhub_PSW | docker login -u $dockerhub_USR --password-stdin'

                sh 'direct_ssh docker push al3xfreeman/randomthought:latest'
            }
        }
        stage('Deploy') {
            steps {
                sh 'direct_ssh docker-compose pull'
                sh 'direct_ssh docker-compose up -d'
            }
        }
        
    }
}