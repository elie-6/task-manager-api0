# Task Management REST API

A RESTful backend service for managing tasks, built with Python, FastAPI and MongoDB.
The project demonstrates clean API design, CRUD operations, and data validation.

## Tech Stack

Python 3.12

FastAPI

MongoDB (Atlas)

Docker

Motor (async MongoDB driver)

Pydantic

Uvicorn

## Features
- Create, read, update, and delete tasks
- Task priority and completion status
- Input validation using Pydantic
- Auto-generated Swagger documentation

## API Endpoints
POST   /tasks  
GET    /tasks  
GET    /tasks/{task_id}  
PUT    /tasks/{task_id}  
DELETE /tasks/{task_id}  

## Getting Started

Create and activate virtual environment:

python3.12 -m venv venv
source venv/bin/activate

pip install -r requirements.txt  (Install dependencies)

uvicorn app.main:app --reload  (Run the API)

