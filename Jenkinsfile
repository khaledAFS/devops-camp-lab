pipeline {
    agent any
    environment {
        HARBOR_REGISTRY = 'harbor.dev.afsmtddso.com'
        HARBOR_REPOSITORY = 'devsecops-lab'
    }
    stages {
        stage('Application docker build') {
            steps {
                echo 'Building application image'
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
                echo 'Building database image'
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
        stage('Test: Scan docker images') {
            environment {
                APP_IMAGE = 'lab'
                DB_IMAGE = 'db'
            }
            steps {
                withCredentials([usernamePassword(credentialsId: 'harbor-auth', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                    echo 'Scanning $APP_IMAGE image'
                    sh 'python harbor_scanner.py -i $APP_IMAGE -r $HARBOR_REGISTRY -p $HARBOR_REPOSITORY -c ${USERNAME}:${PASSWORD}'
                    echo 'Scanning $DB_IMAGE image'
                    sh 'python harbor_scanner.py -i $DB_IMAGE -r $HARBOR_REGISTRY -p $HARBOR_REPOSITORY -c ${USERNAME}:${PASSWORD}'
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