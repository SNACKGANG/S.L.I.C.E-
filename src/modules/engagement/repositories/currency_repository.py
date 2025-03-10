from ..models.currency import Currency
from ..models.currency_type import CurrencyType


class CurrencyRepository:
    @staticmethod
    async def add_currencies_user(user_id: int, amount: int, currency_type_id: int):
        currency_type = await CurrencyType.get(id=currency_type_id)

        currency, created = await Currency.get_or_create(user_id=user_id,
                                                         currency_type=currency_type,
                                                         defaults={"amount": 0})

        currency.amount += amount
        await currency.save()
        return currency

    @staticmethod
    async def remove_currencies_user(user_id: int, amount: int, currency_type: str):
        currency = await Currency.get_or_none(user_id=user_id, currency_type=currency_type)
        if currency and currency.amount >= amount:
            currency.amount -= amount
            await currency.save()
            return True
        return False

    @staticmethod
    async def get_currencies(user_id: int, currency_type_id: int):
        currency_type = await CurrencyType.get(id=currency_type_id)
        currency = await Currency.get_or_none(user_id=user_id, currency_type=currency_type)
        return currency.amount if currency else 0

    @staticmethod
    async def create_currency_type(name: str, description: str = None):
        return await CurrencyType.create(name=name, description=description)

    @staticmethod
    async def get_currency_type_by_name(name: str):
        return await CurrencyType.filter(name=name).first()

    @staticmethod
    async def get_all_currency_types():
        all_currencies = await CurrencyType.all()
        return all_currencies
