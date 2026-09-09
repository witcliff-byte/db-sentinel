pipeline {
    agent any

    environment {
        // The agent image installs Debian's default python3 (see ci/jenkins/Dockerfile).
        // Point this at a different interpreter to pin a version -- it must already
        // exist on the agent, so bump the Dockerfile first.
        PYTHON_BIN = 'python3'
        // Pinned: ruff's default rule set shifts between releases and Lint is a
        // binding gate. Rules live in [tool.ruff.lint] in pyproject.toml.
        RUFF_VERSION = '0.16.6'
    }

    parameters {
        string(
            name: 'DBS_TEST_HOST',
            defaultValue: '192.168.122.236',
            description: 'MySQL host for the integration suite (Vagrant guest IP by default)'
        )
        string(
            name: 'DBS_TEST_USER',
            defaultValue: 'backup_user',
            description: 'MySQL user the integration suite connects as'
        )
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
                // The workspace is reused between builds, so a stale .venv would
                // mask dependency changes. Rebuild it every time.
                sh 'rm -rf .venv'
                sh "${PYTHON_BIN} -m venv .venv"
                sh '.venv/bin/python --version'
                sh '.venv/bin/pip install -r requirements.txt'
                sh '.venv/bin/pip install -e .'
            }
        }

        stage('Lint'){
            steps {
                sh ".venv/bin/pip install ruff==${RUFF_VERSION}"
                sh '.venv/bin/ruff check src/ tests/'
            }
        }

        stage('Unit Tests') {
            steps {
                sh '.venv/bin/pytest -v --junitxml=results.xml'
            }
            post {
                always {
                    junit 'results.xml'
                }
            }
        }

        stage('Integration Tests') {
            // env.BRANCH_NAME is only set by multibranch jobs; this is a pipeline-
            // from-SCM job, so fall back to GIT_BRANCH ("origin/main") from checkout.
            when {
                expression {
                    (env.BRANCH_NAME ?: env.GIT_BRANCH ?: '').replaceFirst(/^origin\//, '') == 'main'
                }
            }
            environment {
                DBS_TEST_PASSWORD = credentials('dbs-test-password')
                DBS_TEST_HOST = "${params.DBS_TEST_HOST}"
                DBS_TEST_USER = "${params.DBS_TEST_USER}"
            }
            steps {
                sh '.venv/bin/pytest -m integration -v'
            }
        }

        stage('Deploy') {
            when { branch 'main' }
            environment {
                ANSIBLE_VAULT_PASSWORD_FILE = credentials('ansible-vault-pass')
            }
            steps {
                sh '''
                    ansible-playbook -i ansible/inventory.ini ansible/deploy.yml --check --diff
                '''
            }
        }
    }

    post {
        success { echo '✅ Pipeline succeeded'}
        failure { echo '❌ Pipeline failed'}
    }
}
