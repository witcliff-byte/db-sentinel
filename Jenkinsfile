pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.13'
    }

    options {
        timeout(time: 10, unitt: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Test') {
            steps {
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
                sh '.venv/bin/pip install -e .'
                sh '.venv/bin/pytest -v'
            }
        }

        stage('Integration Tests') {
            environment {
                DBS_TEST_PASSWORD = credentials('dbs-test-password')
            }
            steps {
                sh '''
                    DBS_TEST_HOST=192.168.122.236 \
                    DBS_TEST_USER=backup_user \
                    .venv/bin/pytest -m integration -v
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished'
        }
        failure {
            echo 'Tests failed - check the logs'
        }
    }
}
