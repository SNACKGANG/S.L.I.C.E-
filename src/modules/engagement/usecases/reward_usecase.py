from src.modules.engagement.repositories.reward_repository import RewardRepository


class RewardUseCase:
    def __init__(self, repository: "RewardRepository"):
        self.repository = repository

    async def create_reward(self, name: str, value: str, chance: int, limit: int, color: str, image_url: str, currency_id: int):
        await self.repository.create_reward(name, value, chance, limit, color, image_url, currency_id)

    async def update_reward(self, name: str, value: str = None, chance: int = None, limit: int = None,
                            color: str = None, image_url: str = None):
        await self.repository.update_reward(name, value, chance, limit, color, image_url)

    async def delete_reward(self, name: str):
        await self.repository.delete_reward(name)

    async def list_rewards(self):
        return await self.repository.list_rewards()

    async def get_available_rewards(self):
        try:
            rewards = await self.repository.get_all_rewards()
            return [{"id": reward.id, "name": reward.name, "value": reward.value} for reward in rewards]
        except Exception as e:
            raise Exception(f"Failed to retrieve available rewards: {e}")
