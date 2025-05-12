pipeline {
  agent any

  environment {
    DEPLOY_SERVER = 'your.remote.server'
    GIT_CRED_ID     = 'github-credentials' // Stored GitHub PAT (as secret text)
    SSH_CRED_ID     = 'server-ssh' // Stored SSH credentials
    VERSION         = "${env.GIT_TAG_NAME ?: 'latest'}"
  }

  stages {
    stage('Checkout Code') {
      steps {
        echo "Cloning repository using GitHub PAT..."
        checkout([
          $class: 'GitSCM',
          branches: [[name: '*/main']],
          doGenerateSubmoduleConfigurations: false,
          extensions: [],
          userRemoteConfigs: [[
            url: 'https://github.com/dhananjayshk/multi-lang-monorepo.git ',
            credentialsId: env.GIT_CRED_ID
          ]]
        ])
      }
    }

    stage('Run Database Migrations') {
      steps {
        script {
          sshagent([env.SSH_CRED_ID]) {
            sh """
              set -ex
              cd \$(mktemp -d)
              cp -r ${WORKSPACE}/db/migrations .
              scp -o StrictHostKeyChecking=no migrations user@${DEPLOY_SERVER}:/tmp/
              ssh -o StrictHostKeyChecking=no user@${DEPLOY_SERVER} '
                cd /opt/multi-lang-monorepo/python-service &&
                docker run --rm \\
                  -v \$(pwd):/app \\
                  -w /app python:3.12-slim \\
                  bash -c "pip install alembic && alembic upgrade head"
              '
            """
          }
        }
      }
    }

    stage('Build and Push Docker Images') {
  steps {
    script {
      def services = ['python-service', 'go-service', 'java-service', 'rust-service']
      withCredentials([usernamePassword(
          usernameVariable: 'DOCKER_USER',
          passwordVariable: 'DOCKER_PASS',
          credentialsId: 'docker-hub-credentials'
      )]) {
        services.each { svc ->
          sh """
            docker build -t yourdockerhub/${svc}:${VERSION} ${svc}
            docker login -u \$DOCKER_USER -p \$DOCKER_PASS
            docker push yourdockerhub/${svc}:${VERSION}
          """
        }
      }
    }
  }
}

    stage('Deploy Services') {
      steps {
        sshagent([env.SSH_CRED_ID]) {
          sh """
            ssh -o StrictHostKeyChecking=no user@${DEPLOY_SERVER} '
              mkdir -p /opt/multi-lang-monorepo
              cp ${WORKSPACE}/docker-compose.yml /opt/multi-lang-monorepo/
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
      echo '❌ Deployment failed!'
    }
    success {
      echo '✅ Deployment successful!'
    }
  }
}
