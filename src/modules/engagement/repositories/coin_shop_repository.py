from ..models.coin_shop_model import Shop


class ShopRepository:
    @staticmethod
    async def create_shop(name, description):
        return await Shop.create(name=name, description=description)

    @staticmethod
    async def remove_shop(shop_id):
        shop = await Shop.filter(id=shop_id).first()
        if not shop:
            raise ValueError(f"Loja com ID {shop_id} não encontrada")
        await shop.delete()
        return shop

    @staticmethod
    async def get_all_shops():
        return await Shop.all()

    @staticmethod
    async def get_shop_by_id(shop_id):
        return await Shop.filter(id=shop_id).first()

    @staticmethod
    async def update_shop_message_id(shop_id, message_id, channel_id):
        shop = await Shop.filter(id=shop_id).first()
        if not shop:
            raise ValueError(f"Shop with ID {shop_id} not found")
        shop.message_id = message_id
        shop.channel_id = channel_id
        await shop.save()
        return shop

    @staticmethod
    async def get_all_shop_names_with_ids():
        try:
            shops = await Shop.all()
            return {shop.name: shop.id for shop in shops}
        except Exception as e:
            print(f"Error fetching all shop names with IDs: {e}")
            return {}

    @staticmethod
    async def get_all_shop_ids():
        try:
            shops = await Shop.all()
            return [shop.id for shop in shops]
        except Exception as e:
            print(f"Error fetching all store IDs: {e}")
            return []
