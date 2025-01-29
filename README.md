# FastAPI Caching Microservice

##  Overview

This FastAPI-based microservice provides a caching mechanism for transforming and storing interleaved lists of strings. It supports:

- Creating a payload from two lists of strings, applying a transformation function, caching results, and storing the payload.

- Retrieving a stored payload using a unique identifier.

### Features

- FastAPI framework for building RESTful APIs.

- SQLModel and SQLite for database management.

- Caching of transformation results to improve efficiency.

- Dockerized for easy deployment.

### Project Structure
```
.
├── main.py          # Entry point for FastAPI application
├── database.py      # Database setup and session management
├── models.py        # SQLModel database models
├── schemas.py       # Pydantic request schemas
├── utils.py         # Utility functions (hashing, transformation)
├── routes.py        # API endpoints
└── requirements.txt # Dependencies
```

### Installation & Setup

Prerequisites

`Ensure you have Python installed (>=3.8).`

Install Dependencies

```
pip install -r requirements.txt
```
Run the Application
```
uvicorn main:app --reload
```
#### API Endpoints

1. Create Payload

POST `/payload`

Request Body:
```
{
  "list_1": ["first string", "second string", "third string"],
  "list_2": ["other string", "another string", "last string"]
}
```

Response:
```
{
  "payload_id": "unique_identifier"
}
```
2. Read Payload

GET `/payload/{payload_id}`

Response:
```
{
  "output": "FIRST STRING, OTHER STRING, SECOND STRING, ANOTHER STRING, THIRD STRING, LAST STRING"
}
```

## Running with Docker

Build Docker Image
```
docker build -t fastapi-caching .
```
Run Docker Container
```
docker run -p 8000:8000 fastapi-caching
```

OR 
```
docker-compose up
```

### Testing

Access API documentation:

Swagger UI: http://127.0.0.1:8000/docs

ReDoc: http://127.0.0.1:8000/redoc

To run tests 
```
pytest
```