from loguru import logger
from tortoise.exceptions import IntegrityError

from ..models.users_model import Users


class UserRepository:
    @staticmethod
    async def add_user(
        user_id: int,
        wallet_address: str = None,
        virtual_currency_amount: int = 0,
        user_level: int = 1,
        is_wallet_verified: bool = False,
    ) -> None:
        """
        Adds a new user to the database.
        """
        try:
            await Users.create(
                user_id=user_id,
                wallet_address=wallet_address,
                virtual_currency_amount=virtual_currency_amount,
                user_level=user_level,
                is_wallet_verified=is_wallet_verified,
            )
            logger.success(f"User {user_id} added successfully.")
        except IntegrityError as e:
            logger.error(f"Integrity error when adding user {user_id}: {e}")
        except Exception as e:
            logger.error(f"Unexpected error when adding user {user_id}: {e}")
