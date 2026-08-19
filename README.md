# 🛒 Realtime E-Commerce CI/CD Pipeline

A simple Flask-based e-commerce storefront with a fully automated CI/CD pipeline — every push to `main` builds a Docker image, pushes it to DockerHub, and deploys it live on AWS EC2, with zero manual steps.

## 🔧 Tech Stack

- **App**: Python (Flask)
- **Containerization**: Docker
- **Image Registry**: DockerHub
- **CI/CD**: GitHub Actions (self-hosted runner)
- **Hosting**: AWS EC2 (Ubuntu)

## 🚀 How It Works

```
git push → GitHub Actions triggers
         → Docker image built on EC2 (self-hosted runner)
         → image pushed to DockerHub
         → EC2 pulls the latest image
         → container redeployed automatically
         → app live on port 5000
```

Every code change is automatically built, tested, and deployed — no manual SSH or Docker commands needed after initial setup.

## 📁 Project Structure

```
ecommerce-cicd/
├── app.py                      # Flask app entry point
├── requirements.txt            # Python dependencies
├── Dockerfile                  # Container build instructions
├── templates/
│   └── index.html              # Storefront UI
└── .github/
    └── workflows/
        └── main.yml             # CI/CD pipeline definition
```

## ⚙️ Setup Guide

### 1. Launch an EC2 instance
- Ubuntu 22.04, t2/t3.micro (free tier eligible)
- Open inbound ports: **22** (SSH), **80** (HTTP), **5000** (app)

```bash
ssh -i your-key.pem ubuntu@<ec2-public-ip>
```

### 2. Install Docker on EC2

```bash
sudo apt update
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -aG docker $USER
newgrp docker
```

### 3. Register a self-hosted GitHub Actions runner

In your repo: **Settings → Actions → Runners → New self-hosted runner** (Linux/x64), then on the EC2 instance:

```bash
mkdir actions-runner && cd actions-runner
curl -o actions-runner-linux-x64-2.336.0.tar.gz -L <download-url-from-github>
tar xzf ./actions-runner-linux-x64-2.336.0.tar.gz
./config.sh --url <your-repo-url> --token <token-from-github>
./run.sh
```

### 4. Add GitHub repo secrets

**Settings → Secrets and variables → Actions**

| Secret | Value |
|---|---|
| `DOCKERHUB_USERNAME` | Your DockerHub username |
| `DOCKERHUB_TOKEN` | DockerHub access token (Account Settings → Security) |

### 5. Push to `main`

The pipeline runs automatically: builds the image, pushes to DockerHub, and redeploys the container on EC2.

## 🌐 Live App

Once deployed, access the app at:

```
http://<your-ec2-public-ip>:5000
```

## 📸 Preview

*(Add a screenshot of the running app here)*

## 📝 Notes

- The self-hosted runner (`./run.sh`) must stay running on EC2 for the pipeline to pick up new jobs.
- EC2 free-tier hours are limited (750 hrs/month) — stop the instance when not in use.
- Stopping/starting the instance may change its public IP unless an Elastic IP is attached.
