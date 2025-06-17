pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps'
        TEST_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps-TestCases'
        APP_IMAGE = 'markdown-blog-app'
        TEST_IMAGE = 'markdown-blog-tests'
        DOCKER_NETWORK = 'markdown_net'
    }

    stages {
        stage('Checkout Application') {
            steps {
                dir('app') {
                    git branch: 'main', url: "${APP_REPO}"
                }
            }
        }

        stage('Checkout Tests') {
            steps {
                dir('tests') {
                    git branch: 'main', url: "${TEST_REPO}"
                }
            }
        }

        stage('Create Docker Network') {
            steps {
                script {
                    sh "docker network inspect ${DOCKER_NETWORK} >/dev/null 2>&1 || docker network create ${DOCKER_NETWORK}"
                }
            }
        }

        stage('Build Application Docker Image') {
            steps {
                dir('app') {
                    script {
                        sh "docker build -t ${APP_IMAGE} ."
                    }
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    script {
                        sh "docker build -t ${TEST_IMAGE} ."
                    }
                }
            }
        }

        stage('Start Application Container') {
            steps {
                script {
                    sh """
                        echo "Cleaning up any old containers..."
                        docker rm -f markdown-app || true

                        echo "🚀 Starting application container..."
                        docker run -d --name markdown-app --network ${DOCKER_NETWORK} ${APP_IMAGE}

                        echo "⏳ Waiting for application to become available..."
                        for i in {1..10}; do
                            if docker run --rm --network ${DOCKER_NETWORK} curlimages/curl:7.85.0 curl -s markdown-app:3000 > /dev/null; then
                                echo "✅ App is available."
                                break
                            else
                                echo "⏳ Still waiting..."
                                sleep 2
                            fi
                        done
                    """
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    sh """
                        echo "🧪 Running Selenium tests against app..."
                        docker run --rm --network ${DOCKER_NETWORK} ${TEST_IMAGE}
                    """
                }
            }
        }
    }

    post {
        success {
            echo '✅ Mark-Down-Blog application and tests ran successfully.'
        }
        failure {
            echo '❌ Mark-Down-Blog pipeline failed.'
        }
    }
}
