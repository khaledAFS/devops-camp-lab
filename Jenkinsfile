pipeline {
    agent any
    environment {
        HARBOR_REGISTRY = 'harbor.dev.afsmtddso.com'
        HARBOR_REPOSITORY = 'devsecops-lab'
    }
    stages {
        stage('Application docker build') {
            steps {
                withCredentials([usernameColonPassword(credentialsId: 'harbor-auth', variable: 'HARBOR-AUTH')]) {
                    script{
                        docker.build('lab')
                        docker.withRegistry('https://$HARBOR_REGISTRY', 'harbor-auth') {
                            sh 'docker tag lab $HARBOR_REGISTRY/$HARBOR_REPOSITORY/lab:latest'
                            sh 'docker push $HARBOR_REGISTRY/$HARBOR_REPOSITORY/lab:latest'
                        }
                    }
                }
            }
        }
        stage('Database docker build') {
            steps {
                withCredentials([usernameColonPassword(credentialsId: 'harbor-auth', variable: 'HARBOR-AUTH')]) {
                    script{
                        docker.build('db', '-f dbDockerfile .')
                        docker.withRegistry('https://$HARBOR_REGISTRY', 'harbor-auth') {
                            sh 'docker tag db $HARBOR_REGISTRY/$HARBOR_REPOSITORY/db:latest'
                            sh 'docker push $HARBOR_REGISTRY/$HARBOR_REPOSITORY/db:latest'
                        }
                    }
                }
            }
        }
        stage('Test') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-auth', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    sh 'python harbor_scanner.py -i nginx -r $HARBOR_REGISTRY -p $HARBOR_REPOSITORY -c ${USERNAME}:${PASSWORD}'
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deployment stage'
            }
        }
    }
    post {
        cleanup {
            echo 'Post actions'
        }
    }
}