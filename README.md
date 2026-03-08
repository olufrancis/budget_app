# BudgetFlow App 💰

A Flask-based budgeting web application deployed using a full DevOps pipeline.

## Tech Stack
- **App**: Python Flask
- **Infrastructure**: Terraform (AWS EC2 t2.micro)
- **Configuration**: Ansible
- **Containerization**: Kubernetes (Minikube)
- **Monitoring**: Prometheus + Grafana
- **CI/CD**: GitHub Actions
- **Scripting**: Bash

## Project Structure
- `app/` - Flask web application
- `terraform/` - AWS infrastructure provisioning
- `ansible/` - Server configuration and deployment
- `kubernetes/` - Kubernetes manifests
- `monitoring/` - Prometheus and Grafana configs
- `scripts/` - Bash automation scripts
- `.github/workflows/` - CI/CD pipeline


## Quick Start
```bash
cd app
pip install -r requirements.txt
python app.py
```

## Author
olufrancis
```
