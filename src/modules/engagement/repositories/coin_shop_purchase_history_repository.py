from tortoise.functions import Sum
from ..models import PurchaseHistory


class PurchaseHistoryRepository:
    @staticmethod
    async def get_user_purchased_quantity(user_id, shop_id, item_id):
        try:
            result = await (PurchaseHistory.filter(
                user_id=user_id, shop_id=shop_id, item_id=item_id)
                            .annotate(total_purchased=Sum("quantity")).first()
                            .values("total_purchased"))

            if result:
                total = result["total_purchased"]
                return total if total is not None else 0
            return 0
        except Exception as e:
            print(f"Error while fetching the item_quantity purchased by the user: {e}")
            return None

    @staticmethod
    async def record_purchase(user_id, item_id, shop_id, quantity, total_price):
        try:
            return await PurchaseHistory.create(user_id=user_id, item_id=item_id, shop_id=shop_id, quantity=quantity, total_price=total_price)
        except Exception as e:
            print(f"Error while recording the purchase in the database: {e}")
            return None
