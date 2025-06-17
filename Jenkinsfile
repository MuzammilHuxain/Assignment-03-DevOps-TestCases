// Jenkinsfile

pipeline {
    agent any // Or a specific agent label if you have one, e.g., agent { label 'docker-host' }

    environment {
        APP_IMAGE = 'markdown-blog-app'
        TEST_IMAGE = 'markdown-blog-tests'
        DOCKER_NETWORK = 'markdown_test_network'
    }

    stages {
        stage('Clean Workspace') {
            steps {
                cleanWs() // Cleans the workspace directory
            }
        }

        stage('Build App Image') {
            steps {
                script {
                    echo "Building Docker image for the Node.js application..."
                    // Assuming your app.js Dockerfile is named Dockerfile.app in the root
                    // If it's just 'Dockerfile' you can remove '-f Dockerfile.app'
                    sh "docker build -t ${APP_IMAGE} -f Dockerfile ."
                }
            }
        }

        stage('Build Test Image') {
            steps {
                script {
                    echo "Building Docker image for Selenium tests..."
                    // Assuming your selenium_test.py Dockerfile is in a 'tests' directory
                    // and named Dockerfile.selenium. Adjust path and filename as needed.
                    sh "docker build -t ${TEST_IMAGE} -f selenium_test.py.dockerfile ."
                }
            }
        }

        stage('Run End-to-End Tests') {
            steps {
                script {
                    echo "Setting up Docker network and running tests..."

                    // Ensure previous containers/networks are cleaned up before starting
                    // The '|| true' allows the command to fail without failing the pipeline
                    sh "docker rm -f ${APP_IMAGE} || true"
                    sh "docker network rm ${DOCKER_NETWORK} || true"

                    // Create a dedicated Docker network for inter-container communication
                    sh "docker network create ${DOCKER_NETWORK}"

                    try {
                        // Start the Node.js application container
                        // --name: Assigns a name for easy reference and network resolution
                        // --network: Connects the container to our custom network
                        // -p 3000:3000: (Optional) Publishes port 3000 from container to host.
                        //              Not strictly needed for inter-container comms on same network,
                        //              but useful for local debugging or external access.
                        sh "docker run -d --name ${APP_IMAGE} --network ${DOCKER_NETWORK} -p 3000:3000 ${APP_IMAGE}"

                        // Wait for the Node.js application to fully start
                        // Adjust sleep duration or consider implementing a robust health check
                        echo "Waiting for Node.js app to start..."
                        sleep 15 // Increased sleep slightly for robustness

                        // Run the Selenium tests container
                        // --rm: Automatically remove the container when it exits
                        // --network: Connects the test container to the same network
                        sh "docker run --rm --network ${DOCKER_NETWORK} ${TEST_IMAGE}"

                    } catch (Exception e) {
                        // Catch any errors during the test execution
                        echo "Tests failed: ${e.message}"
                        currentBuild.result = 'FAILURE'
                        throw e // Re-throw to mark the stage as failed
                    } finally {
                        // Clean up: Stop and remove the Node.js app container and the network
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