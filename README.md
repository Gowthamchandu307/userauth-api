# FastAPI User Authentication System

This project implements a user registration and authentication system using FastAPI, SQLAlchemy with MySQL database, JWT tokens for authentication, and Docker for containerization.

## Features

- **User Registration API**: Allows new users to register by providing their first name, last name, email, and password.
- **User Login API**: Authenticates users and provides a JWT token for authorized access.
- **Auth API**: Validates the JWT token for secure endpoints.

## Technologies Used

- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQLAlchemy is a SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **MySQL**: MySQL is used as the relational database to store user data.
- **bcrypt**: Library used for password hashing to securely store user passwords.
- **python-jose**: Library for creating and validating JWT tokens for user authentication.
- **Docker**: Docker is used for containerization of the FastAPI application and MySQL database.
- **Docker Compose**: Docker Compose is used to manage the multi-container Docker application.


## Getting Started

### Prerequisites

- Docker and Docker Compose installed on your machine.

### Installation and Setup

1. Clone the repository:

   ```sh
   git clone https://github.com/Gowthamchandu307/userauth-api
   cd userauth-api
  ```
2. Configure environment variables such as database connection details and JWT secret key.

3. Setup Database operations
    ```sh
   python database_operations.py
   ```

4. Build and run the Docker containers:

```sh
docker-compose up --build
```
### API Documentation
Once the application is running, you can access the Swagger documentation at http://localhost:8000/docs to explore and test the APIs provided.




