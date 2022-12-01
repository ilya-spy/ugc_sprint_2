from functools import lru_cache
import aiohttp

from models.user import UserRole, User


class AuthApiService:
    @staticmethod
    async def get_user_role(headers: dict) -> list[UserRole]:
        """
        Запросить Роли Пользователя. Пользователь закодирован в заголовках, с помощью JWT-токена
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("http://auth_api:8000/api/v1/me/roles", headers=headers) as resp:
                response = await resp.json()

        return [UserRole(**item) for item in response]

    @staticmethod
    async def get_user_info(headers: dict) -> User:
        """
        Получить информацию о Пользователе по JWT-токену в заголовке
        """
        async with aiohttp.ClientSession() as session:
            async with session.get("http://auth_api:8000/api/v1/me", headers=headers) as resp:
                response = await resp.json()

        return User(**response)


@lru_cache()
def get_auth_api_service() -> AuthApiService:
    return AuthApiService()
