# Task Management App — From Code to Cloud

A complete DevOps and Cloud deployment project that demonstrates the journey of a Python web application from local development to containerized deployment on Microsoft Azure.

The project includes a FastAPI backend, PostgreSQL database, HTML/CSS/JavaScript frontend, automated testing, Docker, Docker Compose, Jenkins CI, Docker Hub, and deployment to an Azure Virtual Machine.

## Live Application

**Application:** http://40.81.16.105/

The application is deployed on an Azure Ubuntu Virtual Machine and is accessible through the public IP address.

---

## 1. Project Overview

The goal of this project was to build a task management application and demonstrate a complete development-to-cloud workflow.

The project covers:

* Backend API development
* Database integration
* Frontend development
* Automated testing
* Git and GitHub version control
* Docker containerization
* Docker Compose orchestration
* Jenkins Continuous Integration
* Docker Hub image management
* Microsoft Azure networking
* Azure Virtual Machine deployment
* Network security using Azure NSG
* Persistent PostgreSQL storage

The project demonstrates how an application can move from source code on a developer machine to a working cloud deployment.

---

## 2. Technologies Used

### Backend

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn

### Database

* PostgreSQL 16

### Frontend

* HTML
* CSS
* JavaScript
* Nginx

### Testing

* Pytest
* FastAPI TestClient
* HTTPX

### DevOps

* Git
* GitHub
* Docker
* Docker Compose
* Jenkins
* Docker Hub

### Cloud

* Microsoft Azure
* Azure Virtual Network
* Azure Subnet
* Azure Network Security Group
* Azure Virtual Machine
* Ubuntu Server 24.04 LTS

---

# 3. Application Architecture

The application consists of three main services:

```text
                    Internet
                       |
                       |
                Azure Public IP
                40.81.16.105
                       |
                       |
              +------------------+
              |   Azure VM       |
              |  Ubuntu 24.04    |
              +------------------+
                       |
             Docker Compose
                       |
          +------------+------------+
          |            |            |
          v            v            v
     Frontend        FastAPI     PostgreSQL
      Nginx           API           DB
      Port 80       Port 8000     Port 5432
          |            |
          +------------+
                API
```

The frontend is publicly available on port 80.

The FastAPI backend runs on port 8000.

PostgreSQL runs inside the Docker network and is **not publicly exposed**.

---

# 4. Project Structure

```text
task-app/
│
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── tests/
│   └── test_tasks.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   ├── script.js
│   └── Dockerfile
│
├── Dockerfile
├── docker-compose.yml
├── Jenkinsfile
├── requirements.txt
├── .gitignore
└── README.md
```

---

# 5. Backend Development

The backend was developed using FastAPI.

The main application is located at:

```text
app/main.py
```

The API provides endpoints for creating, viewing, updating, and deleting tasks.

## API Endpoints

| Method | Endpoint           | Description      |
| ------ | ------------------ | ---------------- |
| GET    | `/`                | Check API status |
| POST   | `/tasks`           | Create a task    |
| GET    | `/tasks`           | List all tasks   |
| PUT    | `/tasks/{task_id}` | Update a task    |
| DELETE | `/tasks/{task_id}` | Delete a task    |

Example API response:

```json
{
  "message": "Task API is running"
}
```

---

# 6. Database

PostgreSQL 16 is used as the relational database.

The application uses SQLAlchemy as the ORM.

The main database model is:

```text
Task
├── id
├── title
├── description
└── completed
```

The application connects to PostgreSQL using the environment variable:

```text
DATABASE_URL
```

Inside Docker Compose, the database connection is:

```text
postgresql://postgres:postgres@db:5432/tasksdb
```

The hostname `db` refers to the PostgreSQL Docker Compose service.

---

# 7. Persistent Database Storage

PostgreSQL uses a Docker named volume:

```yaml
volumes:
  - postgres_data:/var/lib/postgresql/data
```

This provides persistent database storage.

Therefore, restarting or recreating the PostgreSQL container does not automatically remove the stored task data.

The Docker volume is:

```text
task-app_postgres_data
```

---

# 8. Frontend

The frontend was built using:

* HTML
* CSS
* JavaScript

The frontend communicates with the FastAPI backend.

The JavaScript determines the API host from the current browser hostname:

```javascript
const API_URL = `http://${window.location.hostname}:8000`;
```

This allows the same frontend code to work when accessed through the Azure VM public IP.

The frontend is served by Nginx inside a Docker container.

---

# 9. Testing

Automated tests were created using Pytest and FastAPI TestClient.

The test file is:

```text
tests/test_tasks.py
```

The project currently contains tests for:

1. Creating a task
2. Getting tasks
3. Updating a task
4. Deleting a task

Tests are executed using:

```bash
python -m pytest
```

All four tests passed successfully.

---

# 10. Git and GitHub

Git was used for source code version control.

The project was uploaded to GitHub:

**Repository:** `samkasaju/-task-app`

The Git workflow used in the project was:

```text
Local Development
       |
       v
     Git
       |
       v
    GitHub
```

The `.gitignore` file prevents unnecessary files such as the Python virtual environment, cache files, and environment files from being committed.

Ignored files include:

```text
venv/
__pycache__/
*.pyc
.pytest_cache/
.env
.DS_Store
```

---

# 11. Docker Containerization

The FastAPI backend was containerized using Docker.

Backend Dockerfile:

```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app ./app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

The Docker image is published to Docker Hub as:

```text
samkasaju/task-app:latest
```

---

# 12. Docker Compose

Docker Compose is used to run the complete application stack.

The stack contains:

```text
PostgreSQL
FastAPI
Frontend/Nginx
```

Current service architecture:

```text
frontend
   |
   +---- api
           |
           +---- db
```

### Frontend

```text
Port 80
```

### FastAPI

```text
Port 8000
```

### PostgreSQL

```text
Port 5432
```

PostgreSQL is only available inside the Docker network and is not exposed to the public internet.

---

# 13. Docker Compose Configuration

The main deployment configuration is:

```text
docker-compose.yml
```

The important service configuration is:

```yaml
api:
  image: samkasaju/task-app:latest
  ports:
    - "8000:8000"
```

Frontend:

```yaml
frontend:
  build:
    context: ./frontend
  ports:
    - "80:80"
```

Database:

```yaml
db:
  image: postgres:16
```

---

# 14. Jenkins CI Pipeline

Jenkins was installed and configured to automate the Continuous Integration process.

The Jenkins pipeline is defined in:

```text
Jenkinsfile
```

The pipeline contains the following stages:

```text
Checkout
   ↓
Create Virtual Environment
   ↓
Install Dependencies
   ↓
Run Tests
   ↓
Build Docker Image
   ↓
Push Docker Image
```

### Pipeline Stages

#### 1. Checkout

Jenkins checks out the latest source code from GitHub.

#### 2. Create Virtual Environment

A Python virtual environment is created.

#### 3. Install Dependencies

Dependencies are installed from:

```text
requirements.txt
```

#### 4. Run Tests

Pytest is executed:

```bash
python -m pytest
```

#### 5. Build Docker Image

Jenkins builds:

```text
samkasaju/task-app:latest
```

#### 6. Push Docker Image

The image is pushed to Docker Hub.

---

# 15. Docker Hub

Docker Hub is used as the container image registry.

Repository:

```text
samkasaju/task-app
```

Image:

```text
samkasaju/task-app:latest
```

The deployment workflow is:

```text
GitHub
   |
   v
Jenkins
   |
   +--> Run Tests
   |
   +--> Build Docker Image
   |
   v
Docker Hub
   |
   v
Azure VM
```

The Azure VM pulls the backend image from Docker Hub.

---

# 16. Microsoft Azure Deployment

The application was deployed to Microsoft Azure using an Ubuntu Virtual Machine.

### Azure Resources

| Resource             | Configuration           |
| -------------------- | ----------------------- |
| Resource Group       | `task-app-rg`           |
| Region               | East Asia               |
| Virtual Network      | `task-app-vnet`         |
| VNet Address Space   | `10.0.0.0/16`           |
| Subnet               | `task-app-subnet`       |
| Subnet Address Space | `10.0.1.0/24`           |
| Virtual Machine      | `task-app-vm`           |
| OS                   | Ubuntu Server 24.04 LTS |
| Public IP            | `40.81.16.105`          |

---

# 17. Azure Networking

A dedicated Azure Virtual Network was created:

```text
task-app-vnet
```

Address space:

```text
10.0.0.0/16
```

A subnet was created:

```text
task-app-subnet
```

Subnet range:

```text
10.0.1.0/24
```

The Azure VM was deployed inside this subnet.

Architecture:

```text
Azure VNet
10.0.0.0/16
      |
      +---- Subnet
            10.0.1.0/24
                  |
                  +---- Azure VM
```

---

# 18. Network Security Group

An Azure Network Security Group was configured to control inbound traffic.

The required ports are:

| Port | Purpose     | Access                         |
| ---- | ----------- | ------------------------------ |
| 22   | SSH         | Restricted to administrator IP |
| 80   | Frontend    | Public                         |
| 8000 | FastAPI API | Public for current project     |
| 5432 | PostgreSQL  | Not publicly exposed           |

The PostgreSQL port was intentionally not opened in the Azure NSG.

In addition, the Docker Compose configuration does not publish PostgreSQL's port to the VM host.

This keeps the database internal to the Docker network.

---

# 19. Azure Virtual Machine

The application runs on:

```text
task-app-vm
```

Operating system:

```text
Ubuntu Server 24.04 LTS
```

The VM was configured with Docker and Docker Compose.

Docker was installed and verified.

Docker Compose was also installed and verified.

Git was installed so the application source code could be cloned from GitHub.

---

# 20. Deployment Process

The Azure deployment followed these steps:

### Step 1 — Create Azure resources

Created:

* Resource Group
* Virtual Network
* Subnet
* Network Security Group
* Virtual Machine
* Public IP

### Step 2 — Connect to VM

SSH was used to connect to the Ubuntu VM.

### Step 3 — Install Docker

Docker was installed and configured for the Azure user.

### Step 4 — Clone GitHub repository

The project was cloned from GitHub.

### Step 5 — Pull Docker image

The backend image was pulled from Docker Hub:

```bash
docker pull samkasaju/task-app:latest
```

### Step 6 — Start application

Docker Compose was used:

```bash
docker compose up -d
```

### Step 7 — Verify containers

The running containers were checked with:

```bash
docker ps
```

The final deployment contains:

```text
task-frontend
task-api
task-db
```

---

# 21. Deployment Verification

The FastAPI API was tested from the Azure VM:

```bash
curl http://localhost:8000/
```

The API returned:

```json
{
  "message": "Task API is running"
}
```

The public API was also tested through the Azure public IP:

```bash
curl http://40.81.16.105:8000/
```

The task endpoint was tested:

```bash
curl http://40.81.16.105:8000/tasks
```

The frontend was tested through the public application URL:

```text
http://40.81.16.105/
```

Task creation, completion/update, and deletion were verified through the frontend.

---

# 22. Final Cloud Architecture

The final system can be represented as:

```text
                         Internet
                            |
                            v
                  Azure Public IP
                  40.81.16.105
                            |
                            v
                  Azure Network Security
                         Group
                            |
                            v
                 +---------------------+
                 |     Azure VM        |
                 |   Ubuntu 24.04      |
                 |                     |
                 |   Docker Compose    |
                 +---------------------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        Frontend         FastAPI       PostgreSQL
        Nginx            Container      Container
        Port 80          Port 8000      Port 5432
             |              |
             |              |
             +--------------+
                    |
                    v
               Task Database
                    |
                    v
             Persistent Volume
```

---

# 23. Complete DevOps Workflow

The complete development and deployment workflow is:

```text
Developer
    |
    v
Source Code
    |
    v
Git
    |
    v
GitHub
    |
    v
Jenkins
    |
    +---- Install Dependencies
    |
    +---- Run Pytest
    |
    +---- Build Docker Image
    |
    v
Docker Hub
    |
    v
Azure VM
    |
    v
Docker Compose
    |
    +---- Frontend
    |
    +---- FastAPI
    |
    +---- PostgreSQL
    |
    v
Live Application
```

---

# 24. AWS to Azure Concept Mapping

Although the project was originally considered using AWS, Azure was selected for the final implementation.

The main cloud concepts map as follows:

| AWS            | Azure                         |
| -------------- | ----------------------------- |
| VPC            | Virtual Network               |
| Subnet         | Subnet                        |
| Security Group | Network Security Group        |
| EC2            | Virtual Machine               |
| IAM Role       | Managed Identity              |
| S3             | Blob Storage                  |
| CloudWatch     | Azure Monitor / Log Analytics |
| CloudTrail     | Azure Activity Log            |
| Lambda         | Azure Functions               |
| API Gateway    | Azure API Management          |
| DynamoDB       | Azure Cosmos DB               |

This demonstrates understanding of cloud concepts across different cloud providers.

---

# 25. Security Considerations

Several basic security practices were implemented:

### Database isolation

PostgreSQL is not exposed publicly.

### SSH restriction

SSH access is restricted to the administrator's IP through the Azure NSG.

### Docker credentials

Docker Hub credentials are stored in Jenkins credentials rather than directly inside the Jenkinsfile.

### Environment variables

The database connection string is supplied through an environment variable.

### Git ignore

Sensitive or unnecessary local files such as `.env` and the Python virtual environment are excluded from Git.

---

# 26. Challenges and Solutions

## Challenge 1 — Python dependency issue

The Docker container initially had a PostgreSQL driver mismatch.

The application required the `psycopg` package.

The dependency was corrected to:

```text
psycopg[binary]
```

This resolved the Docker API startup error.

---

## Challenge 2 — Frontend localhost problem

Initially, the frontend JavaScript used:

```javascript
const API_URL = "http://127.0.0.1:8000";
```

When accessed from a remote browser, `127.0.0.1` referred to the user's own computer rather than the Azure VM.

It was changed to:

```javascript
const API_URL = `http://${window.location.hostname}:8000`;
```

This allowed the frontend to communicate with the API running on Azure.

---

## Challenge 3 — Jenkins Java version

Jenkins initially had a Java compatibility issue.

Java 21 was installed and Jenkins was configured to use the Java 21 executable.

Jenkins was then restarted successfully.

---

## Challenge 4 — PostgreSQL exposure

PostgreSQL was initially mapped to the VM host.

For improved security, the host port mapping was removed from Docker Compose.

PostgreSQL now remains accessible only through the Docker network.

---

## Challenge 5 — Frontend public port

The frontend initially used port 5500.

For a cleaner public URL, the deployment was changed to:

```text
80:80
```

The Azure NSG was also updated to allow HTTP traffic on port 80.

The final application can therefore be accessed without specifying a port:

```text
http://40.81.16.105/
```

---

# 27. Current Project Status

The following components have been completed:

* [x] FastAPI backend
* [x] PostgreSQL database
* [x] SQLAlchemy integration
* [x] CRUD API
* [x] Frontend
* [x] Automated tests
* [x] Git repository
* [x] GitHub repository
* [x] Dockerfile
* [x] Docker Compose
* [x] Persistent PostgreSQL volume
* [x] Jenkins installation
* [x] Jenkins pipeline
* [x] Automated testing through Jenkins
* [x] Docker image build through Jenkins
* [x] Docker Hub push
* [x] Azure Resource Group
* [x] Azure VNet
* [x] Azure Subnet
* [x] Azure NSG
* [x] Azure VM
* [x] Docker deployment on Azure
* [x] Public frontend deployment
* [x] API verification
* [x] Database verification
* [x] Final live application

---

# 28. Future Improvements

The current project provides a complete working DevOps and Cloud deployment.

Possible future improvements include:

### Kubernetes

Deploy the application using Kubernetes for container orchestration.

### Azure Kubernetes Service

Move the containers from the VM to Azure Kubernetes Service.

### CI/CD Deployment

Extend Jenkins so that a successful build automatically deploys the latest Docker image to Azure.

### HTTPS

Configure a domain name and HTTPS using TLS certificates.

### Reverse Proxy

Use Nginx as a reverse proxy so that the API can be accessed through the same domain without exposing port 8000 publicly.

For example:

```text
http://example.com/
http://example.com/api/tasks
```

### Managed PostgreSQL

Move PostgreSQL from the VM to Azure Database for PostgreSQL.

### Azure Monitor

Add monitoring, logs, alerts, and dashboards.

### Azure Functions

Use serverless functions for selected background or event-driven tasks.

### Azure API Management

Introduce API Management for API security, policies, monitoring, and rate limiting.

### Cosmos DB

Evaluate Azure Cosmos DB for workloads requiring NoSQL storage and global distribution.

---

# 29. Learning Outcomes

This project provided practical experience with:

* Python backend development
* REST API development
* Database integration
* Automated testing
* Git and GitHub
* Docker
* Docker Compose
* CI pipelines
* Jenkins
* Docker Hub
* Linux server administration
* Azure networking
* NSG security rules
* Virtual Machines
* Cloud deployment
* Application troubleshooting
* Container-based architecture

Most importantly, the project demonstrates the complete path:

```text
Code
  ↓
Test
  ↓
Git
  ↓
GitHub
  ↓
Jenkins
  ↓
Docker
  ↓
Docker Hub
  ↓
Azure
  ↓
Live Application
```

---

# 30. Conclusion

This project successfully demonstrates how a simple task management application can be developed, tested, containerized, integrated into a CI pipeline, published as a Docker image, and deployed to Microsoft Azure.

The final application is running on an Azure Ubuntu Virtual Machine with:

* FastAPI as the backend
* PostgreSQL as the database
* Nginx as the frontend web server
* Docker and Docker Compose for containerization
* Jenkins for Continuous Integration
* Docker Hub for image storage
* Azure VNet, subnet, and NSG for networking and security

The application is publicly accessible at:

**http://40.81.16.105/**

This project represents the complete journey **from code to cloud**.
