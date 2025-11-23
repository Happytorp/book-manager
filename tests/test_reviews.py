import pytest
from httpx import AsyncClient

from app.models.models import Book


@pytest.mark.asyncio
class TestReviews:

    async def test_create_review_success(
            self,
            client: AsyncClient,
            test_book: Book,
            auth_headers: dict
    ):
        """Test successful review creation."""
        response = await client.post(
            f"/books/{test_book.id}/reviews",
            headers=auth_headers,
            json={
                "rating": 5,
                "review_text": "Excellent book!"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["rating"] == 5
        assert data["review_text"] == "Excellent book!"
        # assert data["book_id"] == test_book.id

    async def test_create_review_without_auth(self, client: AsyncClient, test_book: Book):
        """Test review creation without authentication."""
        response = await client.post(
            f"/books/{test_book.id}/reviews",
            json={
                "rating": 5,
                "comment": "Great book!"
            }
        )
        assert response.status_code == 401

    async def test_create_review_invalid_rating(
            self,
            client: AsyncClient,
            test_book: Book,
            auth_headers: dict
    ):
        """Test review with invalid rating."""
        response = await client.post(
            f"/books/{test_book.id}/reviews",
            headers=auth_headers,
            json={
                "rating": 6,  # Rating should be 1-5
                "comment": "Good book"
            }
        )
        assert response.status_code == 422

    async def test_get_book_reviews(
            self,
            client: AsyncClient,
            test_book: Book,
            auth_headers: dict
    ):
        """Test retrieving all reviews for a book."""
        # Create a review first
        await client.post(
            f"/books/{test_book.id}/reviews",
            headers=auth_headers,
            json={"rating": 4, "comment": "Nice book"}
        )

        # Get reviews
        response = await client.get(
            f"/books/{test_book.id}/reviews",
            headers=auth_headers
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)


