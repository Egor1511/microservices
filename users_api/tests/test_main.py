import httpx
import pytest
import respx
from app.config import settings
from app.main import app
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
@respx.mock
async def test_get_user():
    mock_route = respx.get(f"{settings.BASE_URL}/1").mock(
        return_value=httpx.Response(
            200, json={"id": 1, "name": "John Doe", "username": "johndoe", "email": "john.doe@example.com"}
        )
    )

    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as ac:
        response = await ac.get("/users/1")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data
    assert "email" in data
    assert mock_route.called


@pytest.mark.asyncio
@respx.mock
async def test_user_not_found():
    respx.get(f"{settings.BASE_URL}/9999").mock(return_value=httpx.Response(404))

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/users/9999")

    assert response.status_code == 404
    data = response.json()
    assert data["detail"] == "User not found"


@pytest.mark.asyncio
@respx.mock
async def test_external_api_timeout():
    respx.get(f"{settings.BASE_URL}/1").mock(side_effect=httpx.TimeoutException)

    async with AsyncClient(app=app, base_url="http://testserver") as ac:
        response = await ac.get("/users/1")

    assert response.status_code == 500
    data = response.json()
    assert data["detail"] == "Request timed out"
