pipeline {
    agent any

    environment {
        DOCKER_IMAGE = 'yashkrp/restaurant-review'  // Update with your Docker Hub username and repository name
        DOCKER_TAG = 'latest'
        REGISTRY = 'docker.io'  // Docker Hub registry (can be changed for private registries)
    }

    stages {
        stage('Checkout') {
            steps {
                // Checkout code from GitHub repository
                git branch: 'main', url: 'https://github.com/ypanjwani/restaurant-review1.git'  // Replace with your repository URL
            }
        }
        
        stage('Build Docker Image') {
            steps {
                script {
                    // Build Docker image
                    echo "Building Docker image..."
                    sh 'docker build -t ${DOCKER_IMAGE}:${DOCKER_TAG} .'
                }
            }
        }
        
        stage('Run Tests') {
            steps {
                script {
                    // Run tests (if any tests are implemented in your project)
                    echo "Running tests..."
                    // Example: Run unit tests, integration tests, etc. before Docker build
                    // sh 'pytest tests/'  // Uncomment if you have a test suite
                }
            }
        }

        stage('Push to Docker Hub') {
            steps {
                script {
                    // Log in to Docker Hub (if necessary) and push the image
                    echo "Pushing Docker image to Docker Hub..."
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                        sh 'echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin'
                        sh 'docker push ${DOCKER_IMAGE}:${DOCKER_TAG}'
                    }
                }
            }
        }

        stage('Deploy Application') {
            steps {
                script {
                    // Deploy the application to a container or cloud (e.g., AWS, Azure, etc.)
                    echo "Deploying Docker container..."
                    // Example: Run Docker container or deploy to a cloud service
                    // sh 'docker run -d -p 5000:5000 ${DOCKER_IMAGE}:${DOCKER_TAG}'  // Uncomment if you want to deploy locally
                    // Or use cloud-specific deployment commands here
                }
            }
        }
    }

    post {
        always {
            // Cleanup (if any cleanup is needed)
            echo "Cleaning up..."
            // Example: Clean up Docker containers or images after use
            sh 'docker system prune -f'
        }
        
        success {
            echo "Pipeline executed successfully!"
        }
        
        failure {
            echo "Pipeline failed. Investigate the logs for more details."
        }
    }
}
