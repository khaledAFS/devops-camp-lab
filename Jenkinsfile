pipeline {
    agent any
    environment {
        COMMIT_HASH = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
        HARBOR_REGISTRY = 'harbor.dev.afsmtddso.com'
        HARBOR_REPOSITORY = 'devsecops-lab'
        APP_IMAGE_NAME = 'lab'
        DB_IMAGE_NAME = 'db'
    }
    stages {
        stage('Application docker build') {
            steps {
                echo "Building application image"
                withCredentials([usernameColonPassword(credentialsId: 'harbor-auth', variable: 'HARBOR-AUTH')]) {
                    script{
                        docker.build('$APP_IMAGE_NAME')
                        docker.withRegistry('https://$HARBOR_REGISTRY', 'harbor-auth') {
                            sh 'docker tag $APP_IMAGE_NAME $HARBOR_REGISTRY/$HARBOR_REPOSITORY/$APP_IMAGE_NAME:$COMMIT_HASH'
                            sh 'docker push $HARBOR_REGISTRY/$HARBOR_REPOSITORY/$APP_IMAGE_NAME:$COMMIT_HASH'
                        }
                    }
                }
            }
        }
        stage('Database docker build') {
            steps {
                echo "Building database image"
                withCredentials([usernameColonPassword(credentialsId: 'harbor-auth', variable: 'HARBOR-AUTH')]) {
                    script{
                        docker.build('$DB_IMAGE_NAME', '-f dbDockerfile .')
                        docker.withRegistry('https://$HARBOR_REGISTRY', 'harbor-auth') {
                            sh 'docker tag $DB_IMAGE_NAME $HARBOR_REGISTRY/$HARBOR_REPOSITORY/$DB_IMAGE_NAME:$COMMIT_HASH'
                            sh 'docker push $HARBOR_REGISTRY/$HARBOR_REPOSITORY/$DB_IMAGE_NAME:$COMMIT_HASH'
                        }
                    }
                }
            }
        }
        stage('Security scanning') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-auth', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    echo "Scanning $APP_IMAGE_NAME image"
                    sh 'python harbor_scanner.py -i $APP_IMAGE_NAME -r $HARBOR_REGISTRY -p $HARBOR_REPOSITORY -c ${USERNAME}:${PASSWORD}'
                    echo "Scanning $DB_IMAGE_NAME image"
                    sh 'python harbor_scanner.py -i $DB_IMAGE_NAME -r $HARBOR_REGISTRY -p $HARBOR_REPOSITORY -c ${USERNAME}:${PASSWORD}'
                }
            }
        }
        stage('Test'){
            steps {
                echo "Testing stage"
            }
        }
        stage('Deploy') {
            steps {
                echo "Deployment stage"
            }
        }
    }
    post {
        cleanup {
            echo "Post actions"
        }
    }
}