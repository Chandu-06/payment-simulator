pipeline {
    agent any
    environment {
        IMAGE_NAME = "payment-simulator"
        IMAGE_TAG = "latest"
        NAMESPACE = "payment-dev"
    }
    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out code...'
                checkout scm
            }
        }
        stage('Build Image') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .'
            }
        }
        stage('Run Tests') {
            steps {
                sh '''
                    docker run -d --name test-container ${IMAGE_NAME}:${IMAGE_TAG}
                    sleep 3
                    docker exec test-container curl -f http://localhost:8000/health
                    docker stop test-container
                    docker rm test-container
                '''
            }
        }
        stage('Deploy to Minikube') {
            steps {
                sh '''
                    kubectl create namespace ${NAMESPACE} --dry-run=client -o yaml | kubectl apply -f -
                    eval $(minikube docker-env)
                    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    kubectl apply -f deployment.yaml
                    kubectl apply -f service.yaml
                    kubectl rollout status deployment/payment-app -n ${NAMESPACE}
                '''
            }
        }
        stage('Verify') {
            steps {
                sh 'kubectl get pods -n ${NAMESPACE}'
            }
        }
    }
    post {
        always {
            sh 'docker rmi ${IMAGE_NAME}:${IMAGE_TAG} || true'
        }
    }
}
