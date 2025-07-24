[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)
![Current Version](https://img.shields.io/badge/version-0.2.0-blue?style=for-the-badge&logo=python&logoColor=white)
[![Continuous Integration Workflow](https://github.com/josealvarezz/devops-hands-on-project-hivebox/actions/workflows/ci.yml/badge.svg)](https://github.com/josealvarezz/devops-hands-on-project-hivebox/actions/workflows/ci.yml)
[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/josealvarezz/devops-hands-on-project-hivebox/badge)](https://scorecard.dev/viewer/?uri=github.com/josealvarezz/devops-hands-on-project-hivebox)

# HiveBox - DevOps End-to-End Hands-On Project (Personal Fork)

> **Note:** This is my personal fork of the HiveBox project for learning and hands-on DevOps practice.  
> All development is done via Pull Requests on my forked repository. Do not submit PRs to the upstream/original repo.

<p align="center">
  <a href="https://devopsroadmap.io/projects/hivebox" style="display: block; padding: .5em 0; text-align: center;">
    <img alt="HiveBox - DevOps End-to-End Hands-On Project" border="0" width="90%" src="https://devopsroadmap.io/img/projects/hivebox-devops-end-to-end-project.png" />
  </a>
</p>

> [!TIP]
> If you are looking for the full roadmap, including this project, go back to the [getting started](https://devopsroadmap.io/getting-started) page.

This repository is the starting point for [HiveBox](https://devopsroadmap.io/projects/hivebox/), the end-to-end hands-on project.

## Project Status

- [x] Repository forked
- [x] MVP defined
- [x] Tech stack chosen and documented
- [x] Contribution strategy established
- [x] Sensors selected and listed
- [x] Minimal FastAPI app created
- [x] `/version` endpoint implemented
- [x] `/temperature` endpoint implemented (returns average temp from 3 senseBoxes in the last hour)
- [x] Project refactored into `/app` directory
- [x] Unit tests created for `/version` and `/temperature` endpoints (including edge cases and mocks)
- [x] Dockerfile updated to support new structure (`app/main.py`)
- [x] .dockerignore updated and improved
- [x] Can run and test both locally and via Docker
- [x] Continuous Integration (CI) pipeline with linting, testing, and Docker build (only runs on main or PRs to main)
- [x] OpenSSF Scorecard security checks
- [x] senseBox IDs are now configurable via environment variable (`SENSEBOX_IDS`)
- [x] /metrics endpoint implemented, exposing default Prometheus metrics using `prometheus_fastapi_instrumentator`\*\*
- [x] \*\*Added `status` field to `/temperature` endpoint (Too Cold, Good, Too Hot)
- [x] Integration test implemented for `/temperature` endpoint (real API call)
- [x] **Kubernetes manifests created for deployment, service, ingress, NGINX Ingress Controller, and Kind cluster (in `k8s/`)**
- [x] **Can deploy and test HiveBox on a local Kubernetes cluster using Kind**

## How to Run Locally

1. **Create and activate a virtual environment:**
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
3. **Run the application:**
   ```sh
   fastapi dev app/main.py
   ```
   or
   ```sh
   uvicorn app.main:app --reload
   ```
4. **Check the API:**
   - Open [http://localhost:8000/version](http://localhost:8000/version) in your browser.
   - You should see:
     ```json
     { "version": "0.2.0" }
     ```
   - The `/temperature` endpoint returns the average temperature of the 3 selected senseBoxes, if data is less than 1 hour old, and includes a `status` field.
   - The `/metrics` endpoint returns Prometheus metrics about the app.

## Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t hivebox:0.2.0 .
   ```
2. **Run the container (with custom senseBox IDs):**

   ```sh
   docker run --rm -p 8000:80 -e SENSEBOX_IDS="id1,id2,id3" hivebox:0.2.0
   ```

   If you omit `SENSEBOX_IDS`, the default IDs will be used.

3. **Test the API:**
   - Open [http://localhost:8000/version](http://localhost:8000/version)  
     **You should see:**
     ```json
     { "version": "0.2.0" }
     ```
   - Open [http://localhost:8000/temperature](http://localhost:8000/temperature)  
     **You should see (example):**
     ```json
     {
       "temperature": 21.67,
       "status": "Good"
     }
     ```
   - Open [http://localhost:8000/metrics](http://localhost:8000/metrics)

## Kubernetes Deployment

The project includes manifests to deploy HiveBox on a Kubernetes cluster. The files are located in the `k8s/` directory and include:

- `hivebox-deployment.yaml`: Deployment for the HiveBox application.
- `hivebox-service.yaml`: ClusterIP Service to expose the application internally within the cluster.
- `hivebox-ingress.yaml`: Ingress to route HTTP traffic to the HiveBox service using the NGINX Ingress Controller.
- `deploy-ingress-nginx.yaml`: Full manifest to deploy the NGINX Ingress Controller in the cluster.
- `kind-cluster.yaml`: Configuration to create a local Kubernetes cluster using Kind, with port mappings for HTTP (8080) and HTTPS (8443).

These manifests allow you to easily deploy and expose the application in a local or cloud-based Kubernetes environment.

### How to use the Kubernetes manifests

1. **Create a local Kind cluster:**
   ```sh
   kind create cluster --config k8s/kind-cluster.yaml
   ```
2. **Deploy the NGINX Ingress Controller:**
   ```sh
   kubectl apply -f k8s/deploy-ingress-nginx.yaml
   ```
3. **Build and load the Docker image into Kind:**
   ```sh
   docker build -t hivebox:0.2.0 .
   kind load docker-image hivebox:0.2.0
   ```
4. **Deploy HiveBox resources:**
   ```sh
   kubectl apply -f k8s/hivebox-deployment.yaml
   kubectl apply -f k8s/hivebox-service.yaml
   kubectl apply -f k8s/hivebox-ingress.yaml
   ```
5. **Access the API:**
   - Open [http://localhost:8080/version](http://localhost:8080/version) in your browser.
   - The `/temperature` and `/metrics` endpoints are also available at this address.

**Note:**

- You can customize the senseBox IDs by editing the `SENSEBOX_IDS` environment variable in the deployment manifest (`hivebox-deployment.yaml`).
- If you are using a cloud Kubernetes provider, you may need to adapt the manifests (e.g., change the Service type to `LoadBalancer`).

## Continuous Integration

- **ci.yml**: Runs on all pull requests to `main` only.

  - Ensures that all code merged into `main` passes linting, testing, and Docker build checks before being accepted.
  - The workflow covers:
    - Python linting (`pylint`)
    - Dockerfile linting (`hadolint`)
    - Unit and integration testing (`pytest`)
    - Docker image build (verifies Dockerfile and packaging)

- **scorecards-analysis.yml**: Runs only on push to `main`.
  - Performs OpenSSF Scorecard security checks on the latest state of the main branch.
  - Keeps the security badge and repository analysis up to date.

## Testing

1. **Run all tests:**
   ```sh
   pytest
   ```
2. **What is tested:**
   - `/version` endpoint (returns version, always works)
   - `/temperature` endpoint:
     - Happy path (recent data, correct average, correct status)
     - No recent data (returns 404)
     - Some boxes with/without valid data (partial average)
     - Data corrupt or incomplete (ignores those boxes)
     - External API failure (returns 502)
     - Extreme temperature values (calculates average and status)
     - Non-existent senseBox IDs (treated as no data)
   - **Integration test**: Real call to `/temperature` endpoint (may depend on external API availability)

## Endpoints

| Endpoint       | Method | Description                                                                  |
| -------------- | ------ | ---------------------------------------------------------------------------- |
| `/version`     | GET    | Returns current app version                                                  |
| `/temperature` | GET    | Returns current average temperature from 3 senseBoxes, with a `status` field |
| `/metrics`     | GET    | Returns default Prometheus metrics about the app                             |

## Implementation

### MVP Scope

HiveBox builds an API to track environmental data from various sensors using openSenseMap.  
The minimal viable product is an API that returns the same data visible on a given sensor's web page—no logs or historical tracking included.

### Technology Stack Decision

Although most of my previous API experience has been with Java Spring Boot, I have decided to use **FastAPI** for this project.

- The HiveBox documentation recommends Flask or FastAPI.
- I want to broaden my backend skills and try a modern Python-based framework to compare it with my Spring Boot experience.

### Contribution & Branch Strategy

- All main changes are submitted as Pull Requests for each project phase.
- No direct pushes to the `main` branch are allowed.
- **ci.yml** runs on pull requests to `main` (for linting, testing, and build).
- **scorecards-analysis.yml** runs on push to `main` (for security checks).

### senseBox Sensors

These are the three senseBox sensors selected from [openSenseMap](https://opensensemap.org):

- [2729902 Bachstraat](https://opensensemap.org/explore/5c72ec079e6756001987288b)
- [Hesse](https://opensensemap.org/explore/61eec6bf848248001ba4beeb)
- [Aureliahof Utrecht](https://opensensemap.org/explore/61bf38bf19a991001b0e5cb4)

### Decisions Log

- [2025-06-22] Project forked from [HiveBox original repository](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox).
- [2025-06-22] Chosen tech stack: FastAPI (Python) for backend.
- [2025-06-22] Selected 3 senseBox sensors from openSenseMap.
- [2025-06-22] Created minimal FastAPI app and implemented `/version` endpoint as MVP.
- [2025-06-22] Confirmed the app runs and can be tested both locally and via Docker.
- [2025-06-22] Dockerized the app using `fastapi run` as per official docs.
- [2025-06-24] Refactored source code into `app/` directory.
- [2025-06-24] Added `/temperature` endpoint with logic to average latest sensor data from the last hour.
- [2025-06-24] Implemented comprehensive unit tests for endpoints, including edge and error cases.
- [2025-06-24] Updated Dockerfile and .dockerignore for new structure.
- [2025-06-24] Bumped version to 0.1.0 after implementing /temperature and full test suite.
- [2025-06-25] Added GitHub Actions CI pipeline for linting, testing, and Docker build (runs only on main).
- [2025-06-27] Integrated OpenSSF Scorecard workflow
- [2025-07-20] The `/temperature` endpoint now includes a `status` field ("Too Cold", "Good", "Too Hot") based on the average temperature.
- [2025-07-20] The `/metrics` endpoint is implemented using `prometheus_fastapi_instrumentator` to expose default Prometheus metrics.
- [2025-07-20] senseBox IDs are now configurable via the `SENSEBOX_IDS` environment variable, making deployment and containerization more flexible.
- [2025-07-20] Improved error handling: `/temperature` returns 502 if the external API is unreachable, and 404 if there is no recent data.
- [2025-07-20] Added a real integration test for `/temperature`, in addition to unit tests with mocks.
- [2025-07-20] Decided to run CI only on Pull Requests to `main` and Scorecards only on push to `main`, following best workflow practices.
- [2025-07-20] Refactored get_temps in sensebox.py to dynamically search for the temperature sensor by title, removing the dependency on a fixed index and improving robustness.
- [2025-07-24] Added Kubernetes manifests (`k8s/`) for deployment, service, ingress, NGINX Ingress Controller, and Kind cluster configuration. HiveBox can now be easily deployed on Kubernetes.
