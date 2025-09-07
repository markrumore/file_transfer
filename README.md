# Flask Transfer

## Overview

This repository provides a modular Flask-based API for handling file and model transfer operations, with a focus on data science and machine learning workflows. The API is designed to support classification, entity extraction, similarity scoring, and service registration for ML models.

## Features

- **RESTful API** built with Flask and Flask-RESTX for easy integration and documentation.
- **Model Management:** Register, list, and query available models and their metadata.
- **Classification Endpoint:** Submit text for classification using various ML models.
- **Entity Extraction & Similarity:** Endpoints for extracting entities and computing similarities between inputs.
- **Service Registration:** Register new model services and manage their routes and metadata.
- **Health Check:** Simple endpoint to verify service status.
- **Logging & Monitoring:** Integrated logging and optional Elastic APM for performance monitoring.

## Structure

- `flask_transfer/flask_worker/worker_flask_app.py`  
  Main Flask application and API routing.
- `flask_transfer/flask_worker/worker_logic.py`  
  Core logic for handling requests and model inference.
- `flask_transfer/flask_worker/worker_classes_api.py`  
  API schema for classification endpoints.
- `flask_transfer/flask_worker/worker_services_api.py`  
  API schema for service registration.
- `flask_transfer/flask_worker/worker_similarities_api.py`  
  API schema for similarity scoring.
- `flask_transfer/flask_worker/worker_logger.py`  
  Logging utilities.

## Usage

1. Install dependencies:
    ```bash
    pip install flask flask-restx elastic-apm pyfiglet
    ```
2. Set environment variables as needed (`WORKER_URL`, `GATEWAY_URL`, `ADMINKEY`).
3. Run the Flask app:
    ```bash
    python flask_transfer/flask_worker/worker_flask_app.py
    ```
4. Access the API documentation via Swagger UI at `http://localhost:5000/`.

## Endpoints

- `POST /models/`  
  Submit text and model types for classification.
- `GET /models/`  
  List available models and their metadata.
- `GET /health`  
  Health check endpoint.

## Extending

- Add new models by updating the model mapping in `worker_logic.py`.
- Extend API schemas in the respective `*_api.py` files.
- Integrate with S3 or other storage for model management.

## License

MIT License

---