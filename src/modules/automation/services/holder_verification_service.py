import asyncio

import discord
from loguru import logger


class HolderVerificationService:
    """
    Service responsible for verifying the wallet details by querying the Reservoir API.
    """

    def __init__(self, reservoir_api: "ReservoirService"):
        self.reservoir_api = reservoir_api
        self.queue = asyncio.Queue()
        self.worker_task = None

    async def start_worker(self):
        """
        Start the worker to process verification tasks from the queue.
        """
        if self.worker_task is None:
            self.worker_task = asyncio.create_task(self._worker())

    async def _worker(self):
        """
        Worker that consumes tasks from the queue and processes them.
        """
        while True:
            wallet_address, verification_event = await self.queue.get()
            logger.info(f"Processing wallet {wallet_address}")

            nft_count = await self.verify_wallet(wallet_address)
            verification_event.result = nft_count

            verification_event.set()
            self.queue.task_done()

    async def add_task_to_queue(
        self, wallet_address: str, verification_event: asyncio.Event
    ):
        """
        Adds a check task to the queue.
        """
        await self.queue.put((wallet_address, verification_event))

    async def verify_wallet(self, wallet_address: str) -> bool:
        """
        Verifies if the wallet holds the required tokens by making an API call.
        """
        try:
            return await self.reservoir_api.get_nft_ownership(
                wallet_address, "0x739e9b04d8dcd08394c0ef0372333957661712f9"
            )
        except Exception as e:
            logger.error(f"Error verifying wallet {wallet_address}: {e}")
            return False

    async def get_all_holders_for_verification(self, collection_address):
        """
        Fetches all wallet addresses and their associated NFT counts from the Reservoir API.
        """
        try:
            # Fetch all holders from the Reservoir API
            holders_data = await self.reservoir_api.get_all_holders(collection_address)

            # Example: holders_data would be in the format {'wallet_address': nft_count}
            if not holders_data:
                logger.warning("No holders found.")
                return {}

            logger.info(f"Fetched {len(holders_data)} holders.")
            return holders_data
        except Exception as e:
            logger.error(f"Error fetching all holders: {e}")
            return {}

    @staticmethod
    async def create_verification_embed(interaction: discord.Interaction):
        guild_name = interaction.guild.name

        embed = discord.Embed(
            title=f"Welcome to {guild_name}!",
            description=(
                "Welcome to **SLICE**! We use SLICE to securely verify your NFT assets "
                "and give you access to exclusive roles.\n\n"
                "Click the button below to start the verification process. "
                "SLICE will never DM you or ask you to click on any suspicious links."
            ),
            color=discord.Color.default(),
        )

        embed.set_footer(text="Verification by SLICE Bot")

        return embed

    @staticmethod
    async def create_configuration_embed(collection_address: str, roles_data: list):
        """
        Create an embed with the configuration of NFT and load ranges.
        """
        embed = discord.Embed(
            title="Holder Verification Configuration",
            description="Configuration successfully saved!",
            color=discord.Color.green(),
        )

        embed.add_field(name="Collection", value=collection_address, inline=False)

        for min_nft, max_nft, role_id in roles_data:
            role = f"role.id: {role_id}>"
            if max_nft:
                nft_range = f"`{min_nft}-{max_nft}`"
            else:
                nft_range = f"`{min_nft}+`"

            embed.add_field(name=f"🔹 {role}", value=f"NFTs: {nft_range}", inline=False)

        return embed
