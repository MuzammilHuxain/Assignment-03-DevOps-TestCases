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
                        docker system prune -f || true
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

        stage('Setup Docker Compose') {
            steps {
                script {
                    writeFile file: 'docker-compose.yml', text: '''
version: '3.8'

services:
  app:
    build: 
      context: ./app
      dockerfile: Dockerfile
    container_name: markdown-app-''' + env.BUILD_NUMBER + '''
    ports:
      - "3000:3000"
    environment:
      - NODE_ENV=test
      - MONGO_URI=mongodb://mongo:27017/markdown_blog_test
      - SESSION_SECRET=test-secret-key
      - PORT=3000
    depends_on:
      mongo:
        condition: service_started
    networks:
      - app-network
    healthcheck:
      test: ["CMD-SHELL", "curl -f http://localhost:3000/auth/login || exit 1"]
      interval: 15s
      timeout: 10s
      retries: 5
      start_period: 30s

  mongo:
    image: mongo:5.0
    container_name: markdown-mongo-''' + env.BUILD_NUMBER + '''
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
    container_name: markdown-tests-''' + env.BUILD_NUMBER + '''
    depends_on:
      app:
        condition: service_healthy
      mongo:
        condition: service_healthy
    networks:
      - app-network
    environment:
      - BASE_URL=http://app:3000

networks:
  app-network:
    driver: bridge
'''
                }
            }
        }

        stage('Build and Start Services') {
            steps {
                script {
                    sh '''
                        echo "🏗️ Building and starting services..."
                        
                        # Build images
                        docker-compose -p ${COMPOSE_PROJECT_NAME} build --no-cache
                        
                        # Start MongoDB first
                        echo "🍃 Starting MongoDB..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} up -d mongo
                        
                        # Wait for MongoDB to be ready
                        echo "⏳ Waiting for MongoDB to be ready..."
                        timeout 60 docker-compose -p ${COMPOSE_PROJECT_NAME} exec -T mongo mongosh --eval "db.adminCommand('ping')" --quiet
                        
                        # Start the application
                        echo "🚀 Starting application..."
                        docker-compose -p ${COMPOSE_PROJECT_NAME} up -d app
                        
                        # Wait for application health check
                        echo "⏳ Waiting for application to be healthy..."
                        timeout 120 sh -c 'until docker-compose -p ${COMPOSE_PROJECT_NAME} ps app | grep -q "healthy"; do
                            echo "Waiting for app health check..."
                            sleep 5
                        done'
                        
                        echo "✅ All services are ready!"
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
            echo '✅ Mark-Down-Blog application and tests ran successfully.'
        }
        failure {
            echo '❌ Mark-Down-Blog pipeline failed.'
        }
    }
}
    