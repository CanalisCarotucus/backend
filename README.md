# Pinkman

FastAPI project template with async SQLAlchemy, PostgreSQL, and Alembic migrations.

## Project Structure
```
├── alembic/                   # Database migrations
│   ├── versions/              # Migration files
│   └── env.py                 # Alembic environment configuration
├── app/                       # Main application directory
│   ├── api/                   # API route definitions
│   │   ├── hello_world.py     # Hello_world endpoint
│   │   ├── passports.py       # API passports
│   │   └── users.py           # API users
│   ├── core/                  # Core application components
│   │   └── exceptions.py      # Custom exceptions
│   ├── crud/                  # CRUD pipeline
│   │   ├── passports.py       # CRUD passports
│   │   └── users.py           # CRUD users
│   ├── db/                    # Database configuration
│   │   ├── connection.py      # Database engine and session management
│   │   └── models.py          # SQLAlchemy ORM models
│   ├── main.py                # FastAPI application entry point
│   ├── middlewares/           # Middleware components
│   │   └── log.py             # Request logging middleware
│   ├── schemas/               # Pydantic schemas (API models)
│   │   ├── hello_world.py     # Hello world request/response schemas
│   │   ├── errors.py          # Errors request/response schemas
│   │   ├── passports.py       # Passport request/response schemas
│   │   ├── responses.py       # Common response schemas
│   │   └── users.py           # User request/response schemas
├── alembic.ini                 # Alembic configuration file
├── .env                        # Environment variables
├── logs/                       # Application logs directory
├── pyproject.toml              # Python dependencies
├── run.sh                      # Script to run the application                   
├── uv.lock                     # Dependency lock file
└── README.md                   # Project documentation
```

## Prerequisites
- Python 3.12+
- PostgreSQL database
- uv package manager

## Setup

1. **Clone repository**  
   Run the following command to download project:  
   ```bash
   git clone -b simple https://github.com/iismoilov7/pinkman.git
   cd pinkman
   ```

2. **Install Required Packages**  
   Run the following command to install the necessary dependencies:  
   ```bash
   uv sync
   ```

3. **Create a `.env` file**  
   Create a `.env` file in the project root with database connection string:
   ```env
   DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname
   ```

4. **Run Database Migrations**  
   Apply Alembic migrations to create database schema:
   ```bash
   uv run alembic upgrade head
   ```
   
   To create a new migration after modifying SQLAlchemy models:
   ```bash
   uv run alembic revision --autogenerate -m "description"
   ```

5. **Start the Application**  
   Launch the application with the following command:  
   ```bash
   bash run.sh
   ```

## API Documentation

Once the application is running, you can access:
- Swagger UI: http://127.0.0.1:8081/docs
- ReDoc: http://127.0.0.1:8081/redoc

API endpoints are versioned:
- `/api/v1/*` - API version 1 (users without passport data)
- `/api/v2/*` - API version 2 (users with passport data)

## API Endpoints

### API v1
- `GET /api/v1/users` - Get all users (without passport data)
- `GET /api/v1/users/{user_id}` - Get user by ID (without passport data)
- `POST /api/v1/users` - Create user (without passport)
- `PUT /api/v1/users/{user_id}` - Update user
- `DELETE /api/v1/users/{user_id}` - Delete user

### API v2
- `GET /api/v2/users/{user_id}` - Get user by ID (with passport data)
- `POST /api/v2/users` - Create user (with optional passport)
- `PUT /api/v2/users/{user_id}` - Update user (returns with passport data)
- `DELETE /api/v2/users/{user_id}` - Delete user
