pipeline {
    agent any

    environment {
        // Obtiene la versión desde el TAG de Git si existe, si no, usa el número de build
        APP_VERSION = "${env.TAG_NAME ? env.TAG_NAME : '1.0.' + env.BUILD_NUMBER}"
        RELEASE_DIR = "release-${env.APP_VERSION}"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                sh 'pipenv install -r requirements.txt'
                sh 'pipenv install --dev pytest'
            }
        }

        stage('Run Tests') {
            steps {
                sh 'pipenv run pytest'
            }
        }

        stage('Generate Documentation') {
            steps {
                sh 'mkdir -p reports'
                sh 'APP_VERSION=${APP_VERSION} doxygen Doxyfile'
            }
        }

        stage('Package Release') {
            steps {
                sh '''
                    mkdir -p ${RELEASE_DIR}
                    cp app.py Doxyfile Pipfile Pipfile.lock ${RELEASE_DIR}/
                    cp -r reports ${RELEASE_DIR}/ 2>/dev/null || true
                    tar -czvf sistema-alumnos-${APP_VERSION}.tar.gz ${RELEASE_DIR}
                '''
            }
        }
    }

    post {
        always {
            archiveArtifacts artifacts: 'reports/doxygen_warnings.log, *.tar.gz', allowEmptyArchive: true
        }
    }
}