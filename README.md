# Spy Cat Agency API
___

## Project Description

This project is a Django-based API for managing spy cats, their missions, and targets. It provides a RESTful API for managing spy cat operations, including assigning missions, tracking targets, and managing spy cat profiles.

### Key Features
- REST API for CRUD operations on spy cats, missions, and targets
- Integration with TheCatAPI for breed validation
- Mission and target completion tracking
- Salary management for spy cats
- Detailed API documentation


## Prerequisites
Before running the project, ensure you have:

- Python 3.x
- pip (Python package manager)
- Access to TheCatAPI

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/Sergey-Chalyi/djangoRESTFramework_APIForSpyCats.git
   cd djangoRESTFramework_APIForSpyCats
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Apply database migrations:
   ```bash
   python manage.py migrate
   ```

## API Documentation

For testing all the endpoints, please refer to the Postman collection:

[Spy Agency API Postman Collection](./spy-agency-postman.json)

### Endpoints

#### Spy Cats API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/cats/` | List all spy cats |
| POST   | `/api/v1/cats/` | Create a new spy cat |
| GET    | `/api/v1/cats/{id}/` | Get spy cat details |
| PUT    | `/api/v1/cats/{id}/` | Update spy cat's salary |
| DELETE | `/api/v1/cats/{id}/` | Delete a spy cat |

#### Missions API
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/api/v1/missions/` | List all missions |
| POST   | `/api/v1/missions/` | Create a new mission |
| GET    | `/api/v1/missions/{id}/` | Get mission details |
| DELETE | `/api/v1/missions/{id}/` | Delete a mission (only if not assigned) |
| PATCH  | `/api/v1/missions/{id}/assign_cat/` | Assign a cat to a mission |
| PATCH  | `/api/v1/missions/{id}/complete/` | Mark mission as complete |

#### Targets API
| Method | Endpoint | Description |
|--------|----------|-------------|
| PUT/PATCH | `/api/v1/targets/{id}/` | Update target notes |
| PATCH  | `/api/v1/targets/{id}/complete/` | Mark target as complete |


## Development
The project uses Django REST Framework for API development and follows RESTful principles. Key features include:
- Serializer validation for data integrity
- Class-based views for consistent API behavior
- Proper error handling and status codes
- Clear separation of concerns in the codebase

## Error Handling
The API returns appropriate HTTP status codes:
- 200: Successful operation
- 400: Bad request (validation errors)
- 404: Resource not found
- 204: Successful deletion

## Contact
For questions and support:
- Email: ch.sergey.rb@gmail.com