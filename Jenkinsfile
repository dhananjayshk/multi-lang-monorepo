pipeline {
  agent any

  environment {
    DEPLOY_SERVER = 'your.remote.server'
    SSH_CREDENTIALS_ID = 'ssh-credentials-id'
    VERSION = "${env.GIT_TAG_NAME ?: 'latest'}"
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Run Database Migrations') {
      steps {
        sshagent([env.SSH_CREDENTIALS_ID]) {
          sh """
          ssh -o StrictHostKeyChecking=no user@${DEPLOY_SERVER} '
            cd /opt/multi-lang-monorepo/python-service &&
            docker run --rm -v \$(pwd):/app -w /app python:3.12-slim \
            bash -c "pip install -r requirements.txt && alembic upgrade head"
          '
          """
        }
      }
    }

    stage('Build and Push Docker Images') {
      steps {
        script {
          def services = ['python-service', 'go-service', 'java-service', 'rust-service']
          services.each { svc ->
            sh """
            docker build -t yourdockerhub/${svc}:${VERSION} ${svc}
            docker push yourdockerhub/${svc}:${VERSION}
            """
          }
        }
      }
    }

    stage('Deploy Services') {
      steps {
        sshagent([env.SSH_CREDENTIALS_ID]) {
          sh """
          ssh user@${DEPLOY_SERVER} '
            cd /opt/multi-lang-monorepo &&
            docker-compose pull &&
            docker-compose up -d
          '
          """
        }
      }
    }
  }

  post {
    failure {
      echo 'Deployment failed!'
    }
    success {
      echo 'Deployment successful!'
    }
  }
}

