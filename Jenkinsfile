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
		    docker rm -f test-container || true
                    docker run -d --name test-container payment-simulator:latest
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
		    docker build -t ${IMAGE_NAME}:${IMAGE_TAG} .
                    docker save ${IMAGE_NAME}:${IMAGE_TAG} | minikube image load -
                    kubectl apply -f deployment.yaml -n ${NAMESPACE}
                    kubectl apply -f service.yaml -n ${NAMESPACE}
                    kubectl rollout status deployment/payment-app -n ${NAMESPACE} --timeout=120s
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
