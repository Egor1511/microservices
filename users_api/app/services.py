from typing import Any

import httpx
from app.config import settings
from app.logger import logger
from app.schemas import User


async def fetch_user(user_id: int) -> User:
    async with httpx.AsyncClient(timeout=settings.TIMEOUT) as client:
        try:
            response = await client.get(f"{settings.BASE_URL}/{user_id}")
            response.raise_for_status()
        except httpx.TimeoutException:
            logger.error(f"Timeout fetching user with ID {user_id}")
            raise ValueError("Request timed out")
        except httpx.RequestError as exc:
            logger.error(f"Request error: {exc}")
            raise ValueError(f"An error occurred while requesting: {exc}")

        user_data: Any = response.json()
        return User(**user_data)
