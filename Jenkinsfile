pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps'
        TEST_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps-TestCases'
        APP_IMAGE = 'markdown-blog-app'
        TEST_IMAGE = 'markdown-blog-tests'
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

        stage('Build Application Docker Image') {
            steps {
                dir('app') {
                    script {
                        sh 'docker build -t ${APP_IMAGE} .'
                    }
                }
            }
        }

        stage('Build Test Docker Image') {
            steps {
                dir('tests') {
                    script {
                        sh 'docker build -t ${TEST_IMAGE} .'
                    }
                }
            }
        }

        stage('Start Application Container') {
            steps {
                script {
                    sh '''
                        echo "🔄 Cleaning up any old containers on port 3000..."
                        docker rm -f markdown-app || true

                        USED_CONTAINER=$(docker ps --filter "publish=3000" -q)
                        if [ ! -z "$USED_CONTAINER" ]; then
                            docker stop $USED_CONTAINER || true
                            docker rm $USED_CONTAINER || true
                        fi

                        echo "🚀 Starting application container..."
                        docker run -d --name markdown-app -p 3000:3000 ${APP_IMAGE}

                        echo "⏳ Waiting for application to become available..."
                        sleep 10
                    '''
                }
            }
        }

        stage('Run Selenium Tests') {
            steps {
                script {
                    sh '''
                        echo "🧪 Running Selenium tests against app..."
                        docker run --rm --network host ${TEST_IMAGE}
                    '''
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
