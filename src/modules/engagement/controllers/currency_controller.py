from loguru import logger


class CurrencyController:
    def __init__(self, use_case: "CurrencyUseCase"):
        self.use_case = use_case

    async def add_coins(self, admin_id: int, user_id: int, currency_type_id: int, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        try:
            await self.use_case.add_currency(user_id, quantity, currency_type_id)
            logger.info(f"Admin {admin_id} added {quantity} {currency_type_id} to user {user_id}")
        except Exception as e:
            logger.error(f"Failed to add currency: {e}")
            raise

    async def remove_coins(self, admin_id: int, user_id: int, currency_type: str, quantity: int):
        if quantity <= 0:
            raise ValueError("Quantity must be greater than zero.")
        try:
            await self.use_case.remove_currency(user_id, quantity, currency_type)
            logger.info(f"Admin {admin_id} removed {quantity} {currency_type} from user {user_id}")
        except Exception as e:
            logger.error(f"Failed to remove currency: {e}")
            raise

    async def get_balance(self, user_id: int, currency_type_id: int):
        try:
            balance = await self.use_case.get_currency_balance(user_id, currency_type_id)
            logger.info(f"Retrieved balance for user {user_id}: {balance} {currency_type_id}")
            return balance
        except Exception as e:
            logger.error(f"Failed to retrieve balance: {e}")
            raise

    async def get_available_currencies(self):
        try:
            currency_types = await self.use_case.get_all_currency_types()
            return [{"id": currency.id, "name": currency.name} for currency in currency_types]
        except Exception as e:
            logger.error(f"Failed to retrieve available currencies: {e}")
            raise

    async def create_currency_type(self, name: str, description: str = None):
        try:
            await self.use_case.create_currency_type(name, description)
            logger.info(f"Currency type '{name}' created successfully")
        except Exception as e:
            logger.error(f"Failed to create currency type: {e}")
            raise
