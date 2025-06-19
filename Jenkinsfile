pipeline {
    agent any

    environment {
        APP_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps'
        TEST_REPO = 'https://github.com/MuzammilHuxain/Assignment-03-DevOps-TestCases'
        COMPOSE_PROJECT_NAME = "markdown-blog-${BUILD_NUMBER}"
    }

    stages {
        stage('Cleanup') {
            steps {
                script {
                    sh '''
                        echo "🧹 Cleaning up previous containers and networks..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                        docker system prune -f -a --volumes || true
                    '''
                }
            }
        }

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

        stage('Generate Docker Compose File') {
            steps {
                script {
                    writeFile file: 'docker-compose.yml', text: """
version: '3.8'

services:
  app:
    build:
      context: ./app
      dockerfile: Dockerfile
    container_name: markdown-app-${BUILD_NUMBER}
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=test
      - MONGO_URI=mongodb://mongo:27017/markdown_blog_test
      - SESSION_SECRET=test-secret-key
      - PORT=3000
    depends_on:
      mongo:
        condition: service_healthy
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/auth/login || exit 1"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 20s

  mongo:
    image: mongo:5.0
    container_name: markdown-mongo-${BUILD_NUMBER}
    networks:
      - app-network
    tmpfs:
      - /data/db
    healthcheck:
      test: ["CMD", "mongosh", "--eval", "db.adminCommand('ping')"]
      interval: 5s
      timeout: 5s
      retries: 3
      start_period: 5s

  tests:
    build:
      context: ./tests
      dockerfile: Dockerfile
    container_name: markdown-tests-${BUILD_NUMBER}
    depends_on:
      app:
        condition: service_healthy
      mongo:
        condition: service_healthy
    environment:
      - BASE_URL=http://app:3000
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
"""
                }
            }
        }

        stage('Build and Start Services') {
            steps {
                script {
                    sh '''
                        echo "🏗️ Building images..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} build --no-cache

                        echo "🚀 Starting all services..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} up -d

                        echo "⏳ Waiting for application to become healthy..."
                        timeout 120s sh -c '
                          until docker inspect --format="{{.State.Health.Status}}" markdown-app-${BUILD_NUMBER} | grep -q healthy; do
                            echo "Waiting for app..."
                            sleep 5
                          done
                        '

                        echo "✅ Application is healthy!"
                    '''
                }
            }
        }

        stage('Run Tests') {
            steps {
                script {
                    sh '''
                        echo "🧪 Running Selenium tests..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} run --rm tests
                    '''
                }
            }
        }
    }

    post {
        always {
            script {
                sh '''
                    echo "📋 Collecting logs..."
                    docker-compose -p ${COMPOSE_PROJECT_NAME} logs app || true
                    docker-compose -p ${COMPOSE_PROJECT_NAME} logs mongo || true

                    echo "🧹 Cleaning up containers and networks..."
                    docker-compose -p ${COMPOSE_PROJECT_NAME} down --volumes --remove-orphans || true
                '''
            }
        }
        success {
            echo '✅ Markdown-Blog application and tests ran successfully.'
        }
        failure {
            echo '❌ Markdown-Blog pipeline failed.'
        }
    }
}
