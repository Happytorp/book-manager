# Book Manager API

An intelligent book management system built with FastAPI, PostgreSQL, Redis caching, and GROQ LLM integration for generating book summaries and recommendations.

## Features

- **Complete CRUD Operations**: Add, retrieve, update, and delete books
- **Review System**: Users can add reviews and ratings for books
- **AI-Powered Summaries**: Generate book summaries using GROQ LLM model
- **Smart Recommendations**: Get book recommendations based on genre, author, and ratings
- **Redis Caching**: Fast data retrieval with Redis caching layer
- **Asynchronous Operations**: Built with SQLAlchemy AsyncIO and asyncpg for optimal performance
- **Cloud-Ready**: Dockerized application ready for deployment

## Tech Stack

- **Backend**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with async support (asyncpg)
- **Cache**: Redis for high-performance caching
- **ORM**: SQLAlchemy 2.0 with AsyncIO
- **AI Integration**: GROQ LLM API
- **Containerization**: Docker and Docker Compose
- **Testing**: Pytest with async support

## Prerequisites

Before running the project, ensure you have:

- **Docker** and **Docker Compose** installed (for containerized setup)
- **Python 3.11+** (for local development)
- **PostgreSQL 15+** (for local development without Docker)
- **Redis 7+** (for local development without Docker)
- **GROQ API Key** - Get your free API key from [GROQ Console](https://console.groq.com/)

## API Endpoints

### Books
- `POST /books` - Add a new book
- `GET /books` - Retrieve all books
- `GET /books/{id}` - Retrieve a specific book
- `PUT /books/{id}` - Update a book
- `DELETE /books/{id}` - Delete a book

### Reviews
- `POST /books/{id}/reviews` - Add a review for a book
- `GET /books/{id}/reviews` - Get all reviews for a book
- `GET /books/{id}/summary` - Get book summary with aggregated ratings

### AI & Recommendations
- `POST /generate-summary` - Generate AI-powered book summary using GROQ LLM
- `GET /recommendations` - Get book recommendations based on preferences

### Health & Info
- `GET /health_check` - Health check endpoint

## Quick Start

### Option 1: Using Docker Compose (Recommended)

This method will automatically set up PostgreSQL, Redis, and the FastAPI application.

1. **Clone and navigate to the project**:
  ```bash
  cd /home/10738178@ltimindtree.com/Desktop/assigment/book_manager
  ```

2. **Create a `.env` file** (Optional - for custom configuration):
  ```bash
  touch .env
  ```
 
  Add your configuration (optional, defaults are provided):
  ```env
  # Database Configuration
  DATABASE_URL=postgresql+asyncpg://postgres:123456789@postgres:5432/postgres
 
  # GROQ AI Service
  GROQ_API_KEY=your_groq_api_key_here
 
  # JWT Configuration
  JWT_SECRET=your-secret-key-here
  JWT_ALGORITHM=HS256
  ACCESS_TOKEN_EXPIRE_MINUTES=60
 
  # Application Settings
  APP_NAME=Book Manager API
  DEBUG=false
  ```

3. **Start all services** (PostgreSQL, Redis, and FastAPI app):
  ```bash
  docker-compose up -d
  ```

4. **Check if services are running**:
  ```bash
  docker-compose ps
  ```
 
  You should see three containers running:
  - `book_manager_app` (FastAPI application on port 8000)
  - `book_manager_db` (PostgreSQL on port 5432)
  - `book_manager_redis` (Redis on port 6379)

5. **View logs** (optional):
  ```bash
  # View all logs
  docker-compose logs -f
 
  # View specific service logs
  docker-compose logs -f app
  docker-compose logs -f postgres
  docker-compose logs -f redis
  ```

6. **Access the API**:
  - **API Documentation (Swagger)**: http://localhost:8000/docs
  - **Alternative API Docs (ReDoc)**: http://localhost:8000/redoc
  - **API Base URL**: http://localhost:8000
  - **Health Check**: http://localhost:8000/health_check

7. **Stop the services**:
  ```bash
  docker-compose down
  ```

8. **Stop and remove volumes** (removes database data):
  ```bash
  docker-compose down -v
  ```

### Option 2: Local Development Setup

For local development without Docker:

1. **Install PostgreSQL and Redis**:
  ```bash
  # Ubuntu/Debian
  sudo apt-get update
  sudo apt-get install postgresql postgresql-contrib redis-server
 
  # macOS (using Homebrew)
  brew install postgresql redis
 
  # Start services
  sudo systemctl start postgresql
  sudo systemctl start redis
  ```

2. **Create PostgreSQL database**:
  ```bash
  sudo -u postgres psql
  CREATE DATABASE book_manager;
  CREATE USER postgres WITH PASSWORD '123456789';
  GRANT ALL PRIVILEGES ON DATABASE book_manager TO postgres;
  \q
  ```

3. **Clone and navigate to the project**:
  ```bash
  cd /home/10738178@ltimindtree.com/Desktop/assigment/book_manager
  ```

4. **Create and activate virtual environment**:
  ```bash
  python3 -m venv venv
  source venv/bin/activate  # On Windows: venv\Scripts\activate
  ```

5. **Install Python dependencies**:
  ```bash
  pip install -r requirements.txt
  ```

6. **Create `.env` file with your configuration**:
  ```env
  DATABASE_URL=postgresql+asyncpg://postgres:123456789@localhost:5432/book_manager
  GROQ_API_KEY=your_groq_api_key_here
  JWT_SECRET=your-secret-key-here
  ```

7. **Verify Redis is running**:
  ```bash
  redis-cli ping
  # Should return: PONG
  ```

8. **Run the application**:
  ```bash
  uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
  ```

9. **Access the API**:
  - API Documentation: http://localhost:8000/docs
  - Health Check: http://localhost:8000/health_check

## Configuration

### Environment Variables

The application uses the following environment variables (with defaults):

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection string | `postgresql+asyncpg://postgres:123456789@localhost:5432/postgres` |
| `GROQ_API_KEY` | GROQ AI API key for LLM features | Required for AI features |
| `JWT_SECRET` | Secret key for JWT token generation | `change-me-in-production` |
| `JWT_ALGORITHM` | JWT algorithm | `HS256` |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | `60` |
| `APP_NAME` | Application name | `Book Manager API` |
| `DEBUG` | Debug mode | `false` |

### Getting GROQ API Key

1. Visit [GROQ Console](https://console.groq.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new API key
5. Copy the key and add it to your `.env` file or `app/config.py`

### Redis Configuration

Redis is used for caching to improve performance:
- **Host**: `localhost` (local) or `redis` (Docker)
- **Port**: `6379`
- **Cache TTL**: 300 seconds (5 minutes) by default
- **Connection**: Async Redis client with JSON encoding

The Redis cache is automatically configured and requires no additional setup when using Docker Compose.

## Docker Services

The `docker-compose.yml` file sets up three services:

### 1. PostgreSQL Database
- **Container**: `book_manager_db`
- **Image**: `postgres:15`
- **Port**: `5432`
- **Credentials**:
 - User: `postgres`
 - Password: `123456789`
 - Database: `postgres`

### 2. Redis Cache
- **Container**: `book_manager_redis`
- **Image**: `redis:7`
- **Port**: `6379`
- **Persistence**: Enabled with AOF (Append Only File)

### 3. FastAPI Application
- **Container**: `book_manager_app`
- **Port**: `8000`
- **Auto-reload**: Enabled for development
- **Depends on**: PostgreSQL (with health check)

## Usage Examples

### Add a Book
```bash
curl -X POST "http://localhost:8000/books/" \
 -H "Content-Type: application/json" \
 -d '{
   "title": "The Great Gatsby",
   "author": "F. Scott Fitzgerald",
   "genre": "Fiction",
   "year_published": 1925,
   "summary": "A classic American novel set in the Jazz Age"
 }'
```

### Get All Books
```bash
curl "http://localhost:8000/books/"
```

### Generate AI Summary
```bash
curl -X POST "http://localhost:8000/generate-summary" \
 -H "Content-Type: application/json" \
 -d '{
   "title": "1984",
   "author": "George Orwell"
 }'
```

### Get Recommendations
```bash
curl "http://localhost:8000/recommendations?genre=fiction&limit=10"
```

### Add a Review
```bash
curl -X POST "http://localhost:8000/books/1/reviews" \
 -H "Content-Type: application/json" \
 -d '{
   "review_text": "Excellent book!",
   "rating": 5
 }'
```

## Database Schema

### Books Table
- `id` (Primary Key)
- `title` (Text, Required)
- `author` (String, Required)
- `genre` (String, Optional)
- `year_published` (Integer, Optional)
- `summary` (Text, Optional)
- `reviews` (Relationship → Reviews)

### Reviews Table
- `id` (Primary Key)
- `book_id` (Foreign Key → books.id)
- `user_id` (Foreign Key → users.id)
- `review_text` (Text, Optional)
- `rating` (Integer, 1-5, Required)
- `created_at` (Timestamp)

### Users Table
- `id` (Primary Key)
- `username` (String, Unique, Required)
- `email` (String, Unique, Required)
- `hashed_password` (String, Required)
- `role` (String, Default: "user")
- `reviews` (Relationship → Reviews)

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/ -v --asyncio-mode=auto

# Run specific test file
pytest tests/test_books.py -v

# Run with coverage
pytest tests/ --cov=app --cov-report=html
```

## Project Structure

```
book_manager/
├── app/
│   ├── api/
│   │   └── routers/          # API route handlers
│   ├── db/                   # Database configuration
│   ├── models/               # SQLAlchemy models
│   ├── schemas/              # Pydantic schemas
│   ├── services/             # Business logic
│   │   ├── ai_service.py     # GROQ LLM integration
│   │   ├── book_services.py  # Book operations
│   │   └── review_services.py # Review operations
│   ├── utility/
│   │   └── redis_client.py   # Redis cache client
│   ├── config.py             # Application configuration
│   └── main.py               # FastAPI application
├── tests/                    # Test suite
├── docker-compose.yml        # Docker Compose configuration
├── Dockerfile                # Docker image definition
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Features Implemented

**Asynchronous Programming**: Complete async implementation with SQLAlchemy AsyncIO and asyncpg

**Database Setup**: PostgreSQL with proper schema for books, reviews, and users 

**Redis Caching**: Fast data retrieval with Redis caching layer  

**GROQ LLM Integration**: AI-powered summary generation using GROQ API 

**RESTful API**: All required endpoints implemented 

**CRUD Operations**: Full Create, Read, Update, Delete functionality 

**Review System**: User reviews and rating aggregation 

**Recommendations**: Smart book recommendations with filtering 

**Authentication**: JWT-based authentication system 

**Cloud Ready**: Docker containerization for easy deployment 

**Testing**: Comprehensive test suite with pytest

