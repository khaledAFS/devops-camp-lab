pipeline {
    agent any
    stages {
        stage('Application docker build') {
            steps {
                // withCredentials([string(credentialsId: 'habor-auth', variable: 'harbor-auth')]) {
                    script{
                        tool name: 'docker'
                        docker.build('test:latest')
                        docker.withServer('https://harbor.dev.afsmtddso.com') {
                            docker.image('test:latest').push('latest')
                        }
                    }
                // }
            }
        }
    }
}