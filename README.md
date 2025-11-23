# Book Manager API

An intelligent book management system built with FastAPI, PostgreSQL, and GROQ LLM integration for generating book summaries and recommendations.

## Features

- **Complete CRUD Operations**: Add, retrieve, update, and delete books
- **Review System**: Users can add reviews and ratings for books
- **AI-Powered Summaries**: Generate book summaries GROQ LLM model
- **Smart Recommendations**: Get book recommendations based on genre, author, and ratings
- **Asynchronous Operations**: Built with SQLAlchemy AsyncIO and asyncpg for optimal performance
- **Cloud-Ready**: Dockerized application ready for deployment

## Tech Stack

- **Backend**: FastAPI with Python 3.11+
- **Database**: PostgreSQL with async support (asyncpg)
- **ORM**: SQLAlchemy 2.0 with AsyncIO
- **AI Integration**: GROQ 
- **Containerization**: Docker and Docker Compose
- **Testing**: Pytest with async support

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
- `POST /generate-summary` - Generate AI-powered book summary
- `GET /recommendations` - Get book recommendations based on preferences

### Health & Info
- `GET /health_check` - Health check

## Quick Start

### Using Docker Compose 

1. **Clone and navigate to the project**:
   ```bash
   cd /path/to/book_manager
   ```

2. **Start all services**:
   ```bash
   docker-compose up -d
   ```


4. **Access the API**:
   - API Documentation: http://localhost:8000/docs
   - API Base: http://localhost:8000
   - Health Check: http://localhost:8000/health_check

### Local Development Setup

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2 **Run the application**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## Configuration

The application uses environment variables for configuration. Create a `.env` file:

```env
# Database
DATABASE_URL=postgresql+asyncpg://username:password@localhost:5432/db_name

# AI Service
GROQ_API_KEY= "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"


# Application
APP_NAME=Book Manager API
DEBUG=false
ENVIRONMENT=development
```

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
- `reviews` (Foreign Key → reviews.id)


### Reviews Table
- `id` (Primary Key)
- `book_id` (Foreign Key → books.id)
- `user_id` (Foreign Key → user.id)
- `review_text` (Text, Optional)
- `rating` (Integer, 1-5, Required)
- `created_at` (Timestamp)


### User Table
- `id` (Primary Key)
- `username` (String, Unique, Required)
- `email` (String, Unique, Required)
- `hashed_password` (String, Required)
- `role` (String, Default: "user")
- `reviews` (Foreign Key → user.id)

## Testing

Run the test suite:
```bash
pytest tests/ -v --asyncio-mode=auto
```

## Deployment

The application is containerized and ready for cloud deployment. The Docker Compose setup includes:
- FastAPI application
- PostgreSQL database
- Redis cache
- GROQ LLM service

For production deployment, update the environment variables and ensure proper security configurations.

## Features Implemented

✅ **Asynchronous Programming**: Complete async implementation with SQLAlchemy AsyncIO and asyncpg  
✅ **Database Setup**: PostgreSQL with proper schema for books and reviews  
✅ **GROQ LLM Integration**: AI-powered summary generation
✅ **RESTful API**: All required endpoints implemented  
✅ **CRUD Operations**: Full Create, Read, Update, Delete functionality  
✅ **Review System**: User reviews and rating aggregation  
✅ **Recommendations**: Smart book recommendations with filtering  
✅ **Cloud Ready**: Docker containerization for easy deployment  
