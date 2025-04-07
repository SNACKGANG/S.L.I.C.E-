from ..models import Item


class ItemRepository:
    @staticmethod
    async def create_item(name, description, category=None, role_id=None):
        return await Item.create(name=name, description=description, category=category, role_id=role_id)

    @staticmethod
    async def remove_item(item_id):
        item = await Item.filter(id=item_id).first()
        if not item:
            raise ValueError(f"Item with ID {item_id} not found")
        await item.delete()
        return item

    @staticmethod
    async def get_all_items():
        return await Item.all()

    @staticmethod
    async def get_item_by_id(item_id):
        return await Item.filter(id=item_id).first()

    @staticmethod
    async def get_item_role_id(item_id):
        try:
            item = await Item.filter(id=item_id).first()
            return item.role_id if item else None
        except Exception as e:
            print(f"Error while fetching the ItemRoleID: {e}")
            return None

    @staticmethod
    async def get_all_items_with_names():
        try:
            items = await Item.all()
            return {item.name: item.id for item in items}
        except Exception as e:
            print(f"Error fetching all item names with IDs: {e}")
            return {}
