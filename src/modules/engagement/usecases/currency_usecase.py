from ..repositories.currency_repository import CurrencyRepository


class CurrencyUseCase:
    def __init__(self, repository: CurrencyRepository):
        self.repository = repository

    async def add_currency(self, user_id: int, amount: int, currency_type_id: int):
        return await self.repository.add_currencies_user(user_id, amount, currency_type_id)

    async def remove_currency(self, user_id: int, amount: int, currency_type_id: int):
        return await self.repository.remove_currencies_user(user_id, amount, currency_type_id)

    async def get_currency_balance(self, user_id: int, currency_type_id: int):
        return await self.repository.get_currencies(user_id, currency_type_id)

    async def create_currency_type(self, name: str, description: str = None):
        existing_currency = await self.repository.get_currency_type_by_name(name)
        if existing_currency:
            raise ValueError(f"Currency type '{name}' already exists.")

        await self.repository.create_currency_type(name, description)

    async def get_all_currency_types(self):
        return await self.repository.get_all_currency_types()
