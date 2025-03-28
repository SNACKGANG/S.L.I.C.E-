from loguru import logger


class RewardController:
    def __init__(self, use_case: "RewardUseCase", currency_controller: "CurrencyController"):
        self.use_case = use_case
        self.currency_controller = currency_controller

    async def create_reward(self, name: str, value: str, chance: int, limit: int, color: str, image_url: str, currency_id: int = None):
        try:
            await self.use_case.create_reward(name, value, chance, limit, color, image_url, currency_id)
            logger.info(f"Reward '{name}' created with value '{value}', chance {chance}%, limit {limit}, color '{color}', and image '{image_url}'")
        except Exception as e:
            logger.error(f"Failed to create reward: {e}")
            raise

    async def update_reward(self, name: str, value: str = None, chance: int = None, limit: int = None, color: str = None, image_url: str = None):
        try:
            await self.use_case.update_reward(name, value, chance, limit, color, image_url)
            logger.info(f"Reward '{name}' updated with values: {value}, {chance}, {limit}, {color}, {image_url}")
        except Exception as e:
            logger.error(f"Failed to update reward: {e}")
            raise

    async def delete_reward(self, name: str):
        try:
            await self.use_case.delete_reward(name)
            logger.info(f"Reward '{name}' deleted")
        except Exception as e:
            logger.error(f"Failed to delete reward: {e}")
            raise

    async def list_rewards(self):
        try:
            rewards = await self.use_case.list_rewards()
            logger.info(f"Retrieved all rewards: {rewards}")
            return [{"name": reward.name, "value": reward.value, "chance": reward.chance} for reward in rewards]
        except Exception as e:
            logger.error(f"Failed to list rewards: {e}")
            raise

    async def get_available_currencies(self):
        try:
            return await self.currency_controller.get_available_currencies()
        except Exception as e:
            logger.error(f"Failed to retrieve available currencies: {e}")
            raise

    async def get_available_rewards(self):
        try:
            return await self.use_case.get_available_rewards()
        except Exception as e:
            logger.error(f"Failed to retrieve available rewards: {e}")
            raise
