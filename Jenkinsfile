pipeline {
    agent any

    stages {
        stage('Checkout') {
            checkout scm
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
