pipeline {
    agent any
    stages {
        stage('Application docker build') {
            steps {
                withCredentials([string(credentialsId: 'habor-auth', variable: 'harbor-auth')]) {
                    script{
                        docker.build('test:latest')
                        docker.withRegistry('https://harbor.dev.afsmtddso.com', 'habor-auth') {
                            docker.image('test:latest').push('latest')
                        }
                    }
                }
            }
        }
    }
}