// Jenkinsfile

pipeline {
    agent any

    environment {
        APP_IMAGE = 'markdown-blog-app'
        TEST_IMAGE = 'markdown-blog-tests'
        DOCKER_NETWORK = 'markdown_test_network'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs()
            }
        }

        stage('Build App Image') {
            steps {
                script {
                    echo "Building Docker image for the Node.js application..."
                    // This command is correct based on your folder structure (Dockerfile in root)
                    sh "docker build -t ${APP_IMAGE} -f Dockerfile ."
                }
            }
        }

        stage('Build Test Image') {
            steps {
                script {
                    echo "Building Docker image for Selenium tests..."
                    // CORRECTED: Pointing to the 'Test Cases' directory for Dockerfile and build context
                    // ASSUMPTION: Your Selenium Dockerfile is named 'Dockerfile.selenium'
                    //             and is located inside the 'Test Cases' directory.
                    //             Also, selenium_test.py and requirements.txt are in 'Test Cases'.
                    sh "docker build -t ${TEST_IMAGE} -f 'Test Cases/Dockerfile.selenium' 'Test Cases/'"
                }
            }
        }

        stage('Run End-to-End Tests') {
            steps {
                script {
                    echo "Setting up Docker network and running tests..."

                    sh "docker rm -f ${APP_IMAGE} || true"
                    sh "docker network rm ${DOCKER_NETWORK} || true"

                    sh "docker network create ${DOCKER_NETWORK}"

                    try {
                        sh "docker run -d --name ${APP_IMAGE} --network ${DOCKER_NETWORK} -p 3000:3000 ${APP_IMAGE}"

                        echo "Waiting for Node.js app to start..."
                        sleep 15

                        // Ensure your selenium_test.py uses "http://markdown-blog-app:3000"
                        sh "docker run --rm --network ${DOCKER_NETWORK} ${TEST_IMAGE}"

                    } catch (Exception e) {
                        echo "Tests failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e
                    } finally {
                        echo "Cleaning up Docker resources..."
                        sh "docker stop ${APP_IMAGE} || true"
                        sh "docker rm ${APP_IMAGE} || true"
                        sh "docker network rm ${DOCKER_NETWORK} || true"
                    }
                }
            }
        }
    }

    post {
        always {
            script {
                if (currentBuild.result == 'FAILURE') {
                    echo "❌ Build Failed."
                } else {
                    echo "✅ Build Succeeded."
                }
            }
        }
    }
}