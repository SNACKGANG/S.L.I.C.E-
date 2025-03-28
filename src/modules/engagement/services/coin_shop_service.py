from discord import Embed, NotFound
from discord.ext import commands
from ..repositories.coin_shop_repository import ShopRepository
from ..repositories.coin_shop_shopitem_repository import ShopItemRepository
from ..repositories.coin_shop_item_repository import ItemRepository
from ..models import Shop


class CoinShopService:
    @staticmethod
    async def create_shop_embed(shop: Shop, url_thumbnail: str, url_image_shop: str):
        """
        Creates an embed for the shop details.
        """
        embed = Embed(title=shop.name, description=shop.description, color=0xfd495c)
        embed.set_thumbnail(url=url_thumbnail)
        embed.set_image(url=url_image_shop)
        return embed

    @staticmethod
    async def edit_shop_embed(embed: Embed, shop_items, db: ItemRepository):
        """
        Edits the given embed with the shop's items.
        """
        try:
            # Clear existing description
            embed.description = ""

            # Add items to the embed description
            for shop_item in shop_items:
                item_id_by_shop_item = shop_item.item_id
                item = await db.get_item_by_id(item_id_by_shop_item)
                item_price = shop_item.price
                item_stock = shop_item.stock
                embed.description += (
                                      f"**{item.name} |** `{item_price} "
                                      f"SNACKS` |** {item_stock} Stock**\n")
            return embed
        except Exception as e:
            print(f"Error while editing the shop embed: {e}")

    @staticmethod
    async def update_shop_message(shop_id, bot: commands.Bot):
        """
        Updates the shop message in the specified Discord channel.
        """
        # Fetch the message ID and channel ID from the database
        shop = await ShopRepository.get_shop_by_id(shop_id)
        message_id = shop.message_id
        channel_id = shop.channel_id
        if message_id and channel_id:
            # Update the message content
            try:
                channel = bot.get_channel(channel_id)
                message = await channel.fetch_message(message_id)
                embed = message.embeds[0]
                items = await ShopItemRepository.get_items_by_shop_id(shop_id)
                new_embed = await CoinShopService.edit_shop_embed(embed, items, ItemRepository)
                await message.edit(embed=new_embed)
            except NotFound:
                # If the message is not found, clear the message ID record for the shop
                await ShopRepository.update_shop_message_id(shop_id, None, None)
            except Exception as e:
                print(f"Error while updating the shop message: {e}")
        else:
            print("Shop message ID not found in the database.")
