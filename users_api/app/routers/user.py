import httpx
from app.logger import logger
from app.schemas import User
from app.services import fetch_user
from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get(
    "/users/{user_id}",
    response_model=User,
    summary="Получить информацию о пользователе",
    description="Этот эндпоинт возвращает информацию о пользователе по ID из внешнего API",
)
async def get_user(user_id: int):
    logger.info(f"Fetching user with ID: {user_id}")
    try:
        user = await fetch_user(user_id)
        logger.info(f"Successfully fetched user: {user_id}")
        return user
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            logger.error(f"User not found: {user_id}")
            raise HTTPException(status_code=404, detail="User not found")
        else:
            raise HTTPException(
                status_code=exc.response.status_code, detail=f"External API error: {exc.response.status_code}"
            )
    except httpx.RequestError:
        logger.error("External API request failed")
        raise HTTPException(status_code=500, detail="External API request failed")
    except ValueError as exc:
        logger.error(str(exc))
        raise HTTPException(status_code=500, detail=str(exc))
