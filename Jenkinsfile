pipeline {
    agent any

    environmen {
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
