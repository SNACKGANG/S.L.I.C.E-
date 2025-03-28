import discord

from src.modules.engagement.repositories.reward_repository import RewardRepository


class MysteryBoxService:
    def __init__(self, use_case: "MysteryBoxUseCase"):
        self.use_case = use_case

    @staticmethod
    async def create_lootbox_embed(reward: str, value: str, member):
        reward_data = await RewardRepository.get_reward_by_name(reward)
        if not reward_data:
            raise ValueError(f"Reward '{reward}' not found!")

        embed_color = int(reward_data.color, 16) if reward_data.color else 0xFFFFFF
        image_url = reward_data.image_url

        embed = discord.Embed(
            title="Opening SNACK Box...",
            description=f"🎉 **Reward:** {reward} - {value}",
            color=embed_color,
        )
        embed.set_author(
            name=member.display_name,
            icon_url=member.avatar.url if member.avatar else None,
        )
        if image_url:
            embed.set_image(url=image_url)

        return embed
