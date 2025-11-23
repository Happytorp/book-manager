import pytest
from httpx import AsyncClient

from app.models.models import Book


@pytest.mark.asyncio
class TestBooks:

    async def test_create_book_success(self, client: AsyncClient, auth_headers: dict):
        """Test successful book creation."""
        response = await client.post(
            "/books/",
            headers=auth_headers,
            json={
                "title": "New Book",
                "author": "Author Name",
                "genre": "Science Fiction",
                "year_published": 2024,
                "summary": "An interesting book"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "New Book"
        assert data["author"] == "Author Name"
        assert data["genre"] == "Science Fiction"

    async def test_create_book_without_auth(self, client: AsyncClient):
        """Test book creation without authentication."""
        response = await client.post(
            "/books/",
            json={
                "title": "New Book",
                "author": "Author Name",
                "genre": "Fiction",
                "year_published": 2024
            }
        )
        assert response.status_code == 401

    async def test_get_all_books(self, client: AsyncClient, test_book: Book, auth_headers: dict):
        """Test retrieving all books."""
        response = await client.get("/books/", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1

    async def test_get_book_by_id(self, client: AsyncClient, test_book: Book, auth_headers: dict):
        """Test retrieving a specific book."""
        response = await client.get(f"/books/{test_book.id}", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_book.id
        assert data["title"] == test_book.title

    async def test_get_nonexistent_book(self, client: AsyncClient, auth_headers: dict):
        """Test retrieving non-existent book."""
        response = await client.get("/books/99999", headers=auth_headers)
        assert response.status_code == 404

    async def test_update_book(self, client: AsyncClient, test_book: Book, auth_headers: dict):
        """Test updating a book."""
        response = await client.put(
            f"/books/{test_book.id}",
            headers=auth_headers,
            json={
                "title": "Updated Title",
                "author": test_book.author,
                "genre": test_book.genre,
                "year_published": test_book.year_published,
                "summary": test_book.summary
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated Title"

    async def test_delete_book(self, client: AsyncClient, test_book: Book, auth_headers: dict):
        """Test deleting a book."""
        response = await client.delete(f"/books/{test_book.id}", headers=auth_headers)
        assert response.status_code == 200

        # Verify book is deleted
        get_response = await client.get(f"/books/{test_book.id}", headers=auth_headers)
        assert get_response.status_code == 404


    async def test_get_recommendations(self, client: AsyncClient, test_book: Book, auth_headers: dict):
        """Test book recommendations."""
        response = await client.get(
            "/recommendations",
            params={"genre": test_book.genre, "limit": 5},
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)