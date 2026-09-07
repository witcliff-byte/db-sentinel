pipeline {
    agent any

    environment {
        PYTHON_VERSION = '3.13'
    }

    options {
        timeout(time: 10, unit: 'MINUTES')
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    triggers {
        pollSCM('H/5 * * * *')
    }

    stages {
        stage('Checkout') { steps { checkout scm } }

        stage('Setup'){
            steps{
                sh 'python3 -m venv .venv'
                sh '.venv/bin/pip install -r requirements.txt'
                sh '.venv/bin/pip install -e .'
            }
        }

        stage('Lint'){
            steps {
                sh '.venv/bin/pip install ruff'
                sh '.venv/bin/ruff check src/ tests/ || true'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '.venv/bin/pytest -v --junitxml=results.xml'
            }
            post {
                always {
                    junit 'result.xml'
                }
            }
        }

        stage('Integration Tests') {
            when {
                branch 'main'
            }
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
        success { echo '✅ Pipeline succeded'}
        failure { echo '❌ Pipeline failed'}
    }
}
