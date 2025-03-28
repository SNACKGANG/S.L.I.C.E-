import random


class MysteryBoxUseCase:
    def __init__(self, repository: "MysteryBoxRepository", reward_repository: "RewardRepository"):
        self.repository = repository
        self.reward_repository = reward_repository

    async def create_mystery_box(self, name: str, channel_id: int):
        try:
            return await self.repository.create_mystery_box(name, channel_id)
        except Exception as e:
            raise Exception(f"Failed to create Mystery Box '{name}': {e}")

    async def update_mystery_box(self, box_id: int, name: str = None, channel_id: int = None):
        try:
            return await self.repository.update_mystery_box(box_id, name=name, channel_id=channel_id)
        except Exception as e:
            raise Exception(f"Failed to update Mystery Box '{box_id}': {e}")

    async def delete_mystery_box(self, box_id: int):
        try:
            return await self.repository.delete_mystery_box(box_id)
        except Exception as e:
            raise Exception(f"Failed to delete Mystery Box '{box_id}': {e}")

    async def assign_reward_to_box(self, box_id: int, reward_id: int):
        try:
            return await self.repository.assign_reward_to_box(box_id, reward_id)
        except Exception as e:
            raise Exception(f"Failed to assign Reward '{reward_id}' to Mystery Box '{box_id}': {e}")

    async def get_rewards_for_box(self, box_id: int):
        try:
            rewards = await self.reward_repository.get_rewards_by_box(box_id)
            return [{"name": reward.name, "value": reward.value, "chance": reward.chance} for reward in rewards]
        except Exception as e:
            raise Exception(f"Failed to retrieve rewards for Mystery Box '{box_id}': {e}")

    async def get_mystery_box_by_channel(self, channel_id: int):
        try:
            return await self.repository.get_mystery_box_by_channel(channel_id)
        except Exception as e:
            raise Exception(f"Failed to retrieve Mystery Box for channel '{channel_id}': {e}")

    async def open_lootbox(self, user_id: int, box_id: int):
        rewards = await self.reward_repository.get_rewards_by_box(box_id)
        if not rewards:
            raise ValueError(f"No rewards configured for MysteryBox {box_id}!")

        reward_names = [reward.name for reward in rewards]
        chances = [reward.chance for reward in rewards]
        selected_reward = random.choices(reward_names, weights=chances)[0]

        reward = await self.reward_repository.get_reward_by_name(selected_reward)
        if reward.limit == 0 or reward.opened_this_month < reward.limit:
            await self.reward_repository.increment_opened_this_month(reward.id)
            await self.repository.record_lootbox_opening(user_id, reward.name)
            return {"reward": reward.name, "value": reward.value, "currency_id": reward.currency_id}
        else:
            fallback_reward = await self.reward_repository.get_reward_by_name("Common")
            return {"reward": fallback_reward.name, "value": fallback_reward.value}
