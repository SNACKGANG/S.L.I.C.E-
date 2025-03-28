from src.modules.engagement.services.mystery_box_service import MysteryBoxService

from loguru import logger


class MysteryBoxController:
    def __init__(self, use_case: "MysteryBoxUseCase", currency_controller: "CurrencyController"):
        self.use_case = use_case
        self.currency_controller = currency_controller

    async def create_mystery_box(self, name: str, channel_id: int):
        try:
            return await self.use_case.create_mystery_box(name, channel_id)
            logger.info(f"Mystery Box '{name}' created for channel '{channel_id}'")
        except Exception as e:
            logger.error(f"Failed to create Mystery Box: {e}")
            raise

    async def update_mystery_box(self, box_id: int, name: str = None, channel_id: int = None):
        try:
            updated_box = await self.use_case.update_mystery_box(box_id, name, channel_id)
            logger.info(f"Mystery Box '{updated_box.id}' updated: {updated_box}")
        except Exception as e:
            logger.error(f"Failed to update Mystery Box: {e}")
            raise

    async def delete_mystery_box(self, box_id: int):
        try:
            await self.use_case.delete_mystery_box(box_id)
            logger.info(f"Mystery Box '{box_id}' deleted")
        except Exception as e:
            logger.error(f"Failed to delete Mystery Box: {e}")
            raise

    async def assign_reward_to_box(self, box_id: int, reward_id: int):
        try:
            await self.use_case.assign_reward_to_box(box_id, reward_id)
            logger.info(f"Reward '{reward_id}' assigned to Mystery Box '{box_id}'")
        except Exception as e:
            logger.error(f"Failed to assign reward to Mystery Box: {e}")
            raise

    async def list_rewards_for_box(self, box_id: int):
        try:
            rewards = await self.use_case.get_rewards_for_box(box_id)
            logger.info(f"Retrieved rewards for Mystery Box '{box_id}': {rewards}")
            print(rewards)
            return rewards
        except Exception as e:
            logger.error(f"Failed to list rewards for Mystery Box: {e}")
            raise

    async def get_mystery_box_by_channel(self, channel_id: int):
        try:
            box = await self.use_case.get_mystery_box_by_channel(channel_id)
            logger.info(f"Retrieved Mystery Box for channel '{channel_id}': {box}")
            return {"id": box.id, "name": box.name} if box else None
        except Exception as e:
            logger.error(f"Failed to retrieve Mystery Box by channel: {e}")
            raise

    async def open_lootbox(self, user_id: int, channel_id: int, member: "discord.Member"):
        try:
            box = await self.use_case.get_mystery_box_by_channel(channel_id)
            if not box:
                return None

            reward_data = await self.use_case.open_lootbox(user_id, box.id)
            if reward_data["currency_id"]:
                await self.currency_controller.add_coins(
                    admin_id="Mystery Box",
                    user_id=user_id,
                    currency_type_id=reward_data["currency_id"],
                    quantity=int(reward_data["value"])
                )
            embed = await MysteryBoxService.create_lootbox_embed(reward_data['reward'], reward_data['value'], member)

            return {
                "embed": embed,
                "box_name": box.name,
                "reward": reward_data["reward"],
            }

        except Exception as e:
            logger.error(f"Failed to open lootbox: {e}")
            raise
