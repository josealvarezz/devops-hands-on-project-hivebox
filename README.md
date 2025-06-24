[![Dynamic DevOps Roadmap](https://img.shields.io/badge/Dynamic_DevOps_Roadmap-559e11?style=for-the-badge&logo=Vercel&logoColor=white)](https://devopsroadmap.io/getting-started/)
[![Community](https://img.shields.io/badge/Join_Community-%23FF6719?style=for-the-badge&logo=substack&logoColor=white)](https://newsletter.devopsroadmap.io/subscribe)
[![Telegram Group](https://img.shields.io/badge/Telegram_Group-%232ca5e0?style=for-the-badge&logo=telegram&logoColor=white)](https://t.me/DevOpsHive/985)
[![Fork on GitHub](https://img.shields.io/badge/Fork_On_GitHub-%2336465D?style=for-the-badge&logo=github&logoColor=white)](https://github.com/DevOpsHiveHQ/devops-hands-on-project-hivebox/fork)
![Current Version](https://img.shields.io/badge/version-0.1.0-blue?style=for-the-badge&logo=python&logoColor=white)

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
     { "version": "0.1.0" }
     ```
   - The `/temperature` endpoint returns the average temperature of the 3 selected senseBoxes, if data is less than 1 hour old.

## Running with Docker

1. **Build the Docker image:**
   ```sh
   docker build -t hivebox:0.1.0 .
   ```
2. **Run the container:**
   ```sh
   docker run --rm -p 8000:80 hivebox:0.1.0
   ```
3. **Test the API:**
   - Open [http://localhost:8000/version](http://localhost:8000/version)
   - Open [http://localhost:8000/temperature](http://localhost:8000/temperature)
   - You should see:
     ```json
     { "version": "0.1.0" }
     ```
     and e.g.
     ```json
     { "temperature": 21.67 }
     ```

## Testing

1. **Run all tests:**
   ```sh
   pytest
   ```
2. **What is tested:**
   - `/version` endpoint (returns version, always works)
   - `/temperature` endpoint:
     - Happy path (recent data, correct average)
     - No recent data (returns 404)
     - Some boxes with/without valid data (partial average)
     - Data corrupt or incomplete (ignores those boxes)
     - External API failure (returns 502)
     - Extreme temperature values (calculates average)
     - Non-existent senseBox IDs (treated as no data)

## Endpoints

| Endpoint       | Method | Description                                           |
| -------------- | ------ | ----------------------------------------------------- |
| `/version`     | GET    | Returns current app version                           |
| `/temperature` | GET    | Returns current average temperature from 3 senseBoxes |

## Implementation

### MVP Scope

HiveBox builds an API to track environmental data from various sensors using openSenseMap.  
The minimal viable product is an API that returns the same data visible on a given sensor's web page—no logs or historical tracking included.

### Technology Stack Decision

Although most of my previous API experience has been with Java Spring Boot, I have decided to use **FastAPI** for this project.

- The HiveBox documentation recommends Flask or FastAPI.
- I want to broaden my backend skills and try a modern Python-based framework to compare it with my Spring Boot experience.

### Contribution & Branch Strategy

- All main changes will be submitted as Pull Requests for each project phase.
- No direct pushes to the `main` branch will be made.

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
