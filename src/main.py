import asyncio
import os

import discord
from discord.ext import commands
from loguru import logger
from tortoise import Tortoise

from src.infrastructure.logging import LoguruConfig
from src.infrastructure.settings import (DATABASE, DISCORD_BOT_TOKEN,
                                         RESERVOIR_API_KEY)
from src.modules.administration.models import Users
from src.modules.administration.repositories.guild_config_repository import \
    GuildConfigRepository
from src.modules.automation.cogs.holder_verification_cog import \
    HolderVerificationCog
from src.modules.automation.cogs.sales_config_cog import SalesConfigCog
from src.modules.automation.cogs.scheduled_webhook_cog import ScheduledWebhookCog
from src.modules.automation.controllers.holder_verification_controller import \
    HolderVerificationController
from src.modules.automation.controllers.sales_controller import SalesController
from src.modules.automation.controllers.scheduled_webhook_controller import ScheduledWebhookController
from src.modules.automation.repositories.holder_verification_config_repository import \
    HolderConfigRepository
from src.modules.automation.repositories.holder_verification_repository import \
    HolderVerificationRepository
from src.modules.automation.services.holder_verification_service import \
    HolderVerificationService
from src.modules.automation.services.sales_notification_service import \
    SalesNotificationService
from src.modules.automation.services.sales_service import SalesService
from src.modules.automation.usecases.holder_fetch_all_usecase import \
    HolderFetchAllUseCase
from src.modules.automation.usecases.holder_verification_usecase import \
    HolderVerificationUseCase
from src.modules.automation.usecases.sales_fetch_usecase import \
    SalesFetchUseCase
from src.modules.automation.usecases.sales_send_usecase import SalesSendUseCase
from src.modules.automation.usecases.scheduled_webhook_usecase import ScheduledWebhookUseCase
from src.modules.automation.views.holder_verification_view import \
    HolderVerificationButtonView
from src.modules.engagement.cogs.coin_shop_cog import CoinShopCog
from src.modules.engagement.cogs.currency_cog import CurrencyCog
from src.modules.engagement.cogs.mystery_box_cog import MysteryBoxCog
from src.modules.engagement.cogs.reward_cog import RewardCog
from src.modules.engagement.controllers.coin_shop_controller import CoinShopController
from src.modules.engagement.controllers.currency_controller import CurrencyController
from src.modules.engagement.controllers.mystery_box_controller import MysteryBoxController
from src.modules.engagement.controllers.reward_controller import RewardController
from src.modules.engagement.repositories.currency_repository import CurrencyRepository
from src.modules.engagement.repositories.mystery_box_repository import MysteryBoxRepository
from src.modules.engagement.repositories.reward_repository import RewardRepository
from src.modules.engagement.usecases.coin_shop_usecase import CoinShopUseCase
from src.modules.engagement.usecases.currency_usecase import CurrencyUseCase
from src.modules.engagement.usecases.mystery_box_usecase import MysteryBoxUseCase
from src.modules.engagement.usecases.reward_usecase import RewardUseCase
from src.modules.engagement.views.coin_shop_buyitem_view import ButtonView
from src.modules.moderation.cogs.captcha_verification_config import \
    CaptchaConfigCog
from src.modules.moderation.cogs.emoji_config_cog import EmojiManagerCog
from src.modules.moderation.cogs.role_management_cog import RoleManagementCog
from src.modules.moderation.cogs.thread_config_cog import ThreadManagerCog
from src.modules.moderation.controllers.captcha_controller import \
    CaptchaController
from src.modules.moderation.repositories.captcha_repository import \
    CaptchaRepository
from src.modules.moderation.services.captcha_embed_service import \
    CaptchaEmbedService
from src.modules.moderation.services.captcha_service import CaptchaService
from src.modules.moderation.usecases.captcha_generate_usecase import \
    CaptchaGenerateUseCase
from src.modules.moderation.usecases.captcha_verify_usecase import \
    CaptchaVerifyUseCase
from src.modules.moderation.views.captcha_button_view import \
    VerificationButtonView
from src.shared.services.discord_service import DiscordService
from src.shared.services.http_client import AioHttpClient
from src.shared.services.reservoir_service import ReservoirService
from src.modules.engagement.repositories import PurchaseHistoryRepository, ShopItemRepository, ShopRepository, ItemRepository


class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        super().__init__(command_prefix="s!", intents=intents)

        self.discord_service = DiscordService(self)
        self.reservoir_service = ReservoirService(
            RESERVOIR_API_KEY, http_client=AioHttpClient()
        )

        # SALES
        self.sales_service = SalesService(self.reservoir_service)
        self.sales_notification_service = SalesNotificationService()

        self.fetch_sales_usecase = SalesFetchUseCase(self.sales_service)
        self.send_sales_usecase = SalesSendUseCase(
            self.discord_service, self.sales_notification_service
        )

        self.sales_controller = SalesController(
            self.fetch_sales_usecase, self.send_sales_usecase
        )

        # CAPTCHA
        self.captcha_verification_repository = CaptchaRepository()
        self.captcha_service = CaptchaService(self)
        self.captcha_verification_service = CaptchaEmbedService()

        self.generate_captcha_usecase = CaptchaGenerateUseCase(
            self.captcha_verification_repository,
            self.captcha_service,
            self.captcha_verification_service,
        )
        self.verify_captcha_usecase = CaptchaVerifyUseCase(
            self.captcha_verification_repository,
            self.captcha_service,
            self.discord_service,
        )

        self.captcha_verification_controller = CaptchaController(
            self.generate_captcha_usecase, self.verify_captcha_usecase
        )
        # HOLDER VERIFICATION
        self.holder_verification_service = HolderVerificationService(
            self.reservoir_service
        )
        self.holder_verification_repository = HolderVerificationRepository()
        self.holder_verification_config_repository = HolderConfigRepository()
        self.holder_verification_usecase = [
            HolderVerificationUseCase(
                self.holder_verification_service,
                self.holder_verification_config_repository,
                self.holder_verification_repository,
            ),
            HolderFetchAllUseCase(
                self.holder_verification_service,
                self.holder_verification_repository,
                self.holder_verification_config_repository,
                self,
            ),
        ]
        self.holder_verification_controller = HolderVerificationController(
            holder_verification_usecase=self.holder_verification_usecase[0],
            holder_fetch_all_usecase=self.holder_verification_usecase[1],
        )

        # CURRENCY
        self.currency_repository = CurrencyRepository()
        self.currency_use_case = CurrencyUseCase(self.currency_repository)
        self.currency_controller = CurrencyController(self.currency_use_case)

        # REWARD
        self.reward_repository = RewardRepository()
        self.reward_use_case = RewardUseCase(self.reward_repository)
        self.reward_controller = RewardController(use_case=self.reward_use_case, currency_controller=self.currency_controller)

        # MYSTERY BOX
        self.mystery_box_repository = MysteryBoxRepository()
        self.mystery_box_use_case = MysteryBoxUseCase(repository=self.mystery_box_repository, reward_repository=self.reward_repository)
        self.mystery_box_controller = MysteryBoxController(self.mystery_box_use_case, currency_controller=self.currency_controller)

        # COIN SHOP
        self.coin_shop_repository = ShopRepository()
        self.shop_item_repository = ShopItemRepository()
        self.item_repository = ItemRepository()
        self.purchase_history_repository = PurchaseHistoryRepository()

        self.coin_shop_use_case = CoinShopUseCase(
            shop_repository=self.coin_shop_repository,
            shop_item_repository=self.shop_item_repository,
            purchase_history_repository=self.purchase_history_repository,
            discord_service=self.discord_service,
            currency_repository=self.currency_repository,
            item_repository=self.item_repository,
            bot=self
        )

        self.coin_shop_controller = CoinShopController(self.coin_shop_use_case)

        # WEBHOOK
        self.scheduled_webhook_usecase = ScheduledWebhookUseCase(self.discord_service)
        self.scheduled_webhook_controller = ScheduledWebhookController(self.scheduled_webhook_usecase)

    async def setup_hook(self) -> None:
        logger.info("Setting up database and logging...")
        await Tortoise.init(config=DATABASE)
        await Tortoise.generate_schemas()

        logger.success("Database initialized successfully.")

        log_config = LoguruConfig()
        log_config.setup_logging()
        logger.success("Logging configured successfully.")

        logger.info("Loading cogs and views...")
        await self.add_cog(CaptchaConfigCog(self, self.captcha_verification_controller))
        await self.add_cog(SalesConfigCog(self, self.sales_controller))
        await self.add_cog(CurrencyCog(self, self.currency_controller))
        await self.add_cog(
            HolderVerificationCog(
                self,
                self.holder_verification_controller,
                self.holder_verification_config_repository,
            )
        )
        await self.add_cog(RewardCog(self, self.reward_controller))
        await self.add_cog(MysteryBoxCog(self, self.mystery_box_controller, reward_controller=self.reward_controller))
        await self.add_cog(CoinShopCog(self, self.coin_shop_controller))
        await self.add_cog(RoleManagementCog(self))
        await self.add_cog(ThreadManagerCog(self))
        await self.add_cog(EmojiManagerCog(self))
        await self.add_cog(ScheduledWebhookCog(self, self.scheduled_webhook_controller))
        # CAPTCHA
        self.add_view(
            VerificationButtonView(
                self.captcha_verification_service, self.captcha_verification_controller
            )
        )
        # HOLDER VERIFICATION
        self.add_view(HolderVerificationButtonView(self.holder_verification_controller))
        logger.success("Cogs and views loaded successfully.")

        await self.holder_verification_service.start_worker()

        # COIN Shop
        shop_ids = await self.coin_shop_repository.get_all_shop_ids()
        coin_shop_view_button = ButtonView(self, self.coin_shop_use_case)
        await coin_shop_view_button.initialize_buttons(shop_ids)
        self.add_view(coin_shop_view_button)

    async def on_ready(self):
        await self.wait_until_ready()
        logger.info("Bot is ready. Starting periodic tasks and syncing commands...")
        await self.sync_commands()

        logger.info("Adding guilds to the database...")
        for guild in self.guilds:
            await GuildConfigRepository.add_guild(guild.id, guild.name)
        logger.success("Guilds added to the database successfully.")

    @staticmethod
    async def on_guild_join(guild):
        for member in guild.members:
            user = await Users.filter(user_id=member.id, guild_id=guild.id).first()
            if not user:
                await Users.create(user_id=member.id, guild_id=guild.id)

    @staticmethod
    async def on_member_join(member):
        user = await Users.filter(user_id=member.id, guild_id=member.guild.id).first()
        if not user:
            await Users.create(user_id=member.id, guild_id=member.guild.id)

    @staticmethod
    async def on_member_remove(member):
        await Users.filter(user_id=member.id, guild_id=member.guild.id).delete()

    async def sync_commands(self):
        logger.info("Syncing commands...")
        await self.tree.sync()
        logger.success("Commands synced successfully.")

    async def load_extensions(self):
        logger.info("Loading extensions...")
        cog_dirs = [
            "modules/automation/cogs",
            "modules/moderation/cogs",
            "modules/engagement/cogs",
        ]

        for cog_dir in cog_dirs:
            if os.path.exists(cog_dir):
                for file in os.listdir(cog_dir):
                    if file.endswith(".py") and file != "__init__.py":
                        try:
                            await self.load_extension(
                                f"{cog_dir.replace('/', '.')}.{file[:-3]}"
                            )
                            logger.success(f"Extension {file} loaded successfully.")
                        except Exception as e:
                            logger.error(f"Error loading extension {file}: {e}")

    async def close(self):
        logger.info("Closing database connections and shutting down the bot...")
        await Tortoise.close_connections()
        await super().close()
        logger.success("Bot shut down successfully.")


bot = MyBot()


async def main():
    logger.info("Starting the bot...")
    await bot.start(DISCORD_BOT_TOKEN)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.warning("Execution interrupted by the user.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
