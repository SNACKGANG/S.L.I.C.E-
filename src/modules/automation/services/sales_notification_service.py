import discord
from loguru import logger


class SalesNotificationService:
    @staticmethod
    async def format_sale_embed(sale) -> discord.Embed:
        """
        Format the sales message as a Discord Embed.
        """
        try:
            embed = discord.Embed(color=discord.Color.default())

            if sale.name:
                embed.title = f"{sale.name} sold!"
            else:
                sale.name = f" "

            if (
                sale.token_id
                and sale.price_native is not None
                and sale.price_usd is not None
            ):
                logger.info(f"Processing the description for sale: {sale.contract}")

                floor_price = sale.collection_data.get("floor_price")
                volume_1day = sale.collection_data.get("volume_1day")
                volume_change = sale.collection_data.get("volume_change")

                floor_price = 0 if floor_price is None else floor_price
                volume_1day = 0 if volume_1day is None else volume_1day
                volume_change = 0 if volume_change is None else volume_change

                difference_price = sale.price_native - floor_price
                difference_price_pct = (
                    (difference_price / floor_price * 100) if floor_price else 0
                )

                seller_short = f"{sale.seller[:4]}...{sale.seller[-4:]}"
                buyer_short = f"{sale.buyer[:4]}...{sale.buyer[-4:]}"

                embed.description = (
                    f"🔗 **Token ID:** [{sale.token_id}](https://opensea.io/assets/ethereum/{sale.contract}/{sale.token_id})\n\n"
                    f"💰 **Sale Price:** {sale.price_native} ETH (${sale.price_usd:.2f})\n"
                    f"🏷️ **Floor Price:** {floor_price} ETH \n"
                    f"📉 **{'Below Floor' if difference_price < 0 else 'Above Floor'}:** "
                    f"{abs(difference_price):.4f} ETH ({difference_price_pct:.2f}% {'⬆️' if difference_price > 0 else '⬇️'})\n\n"
                    f"📈 **24h Volume:** {volume_1day:.2f} ETH ({volume_change:.2f}% {'⬆️' if volume_change > 0 else '⬇️'})\n\n"
                    f"👤 **Seller:** [{seller_short}](https://opensea.io/{sale.seller})  👤 **Buyer:** [{buyer_short}](https://opensea.io/{sale.buyer})"
                )
                logger.info(f"Definied description {embed.description}")

            if sale.image:
                embed.set_image(url=sale.image)

            if sale.timestamp:
                embed.set_footer(
                    text=f"{sale.timestamp.strftime('%d-%b-%Y %H:%M:%S UTC')}"
                )

            return embed
        except Exception as e:
            logger.error(f"Error formatting sale embed: {e}")
            raise
