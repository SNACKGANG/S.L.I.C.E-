from datetime import datetime

from src.modules.engagement.models import MysteryBox, Rewards
from src.modules.engagement.models.mystery_box_history_model import MysteryBoxHistory
from src.modules.administration.models.users_model import Users


class MysteryBoxRepository:
    @staticmethod
    async def create_mystery_box(name: str, channel_id: int):
        return await MysteryBox.create(name=name, channel_id=channel_id)

    @staticmethod
    async def update_mystery_box(box_id: int, name: str = None, channel_id: int = None):
        box = await MysteryBox.get(id=box_id)
        if not box:
            raise ValueError(f"Mystery Box '{box_id}' not found!")

        if name is not None:
            box.name = name
        if channel_id is not None:
            box.channel_id = channel_id

        await box.save()
        return box

    @staticmethod
    async def get_mystery_box_by_channel(channel_id: int):
        return await MysteryBox.get_or_none(channel_id=channel_id)

    @staticmethod
    async def list_mystery_boxes():
        return await MysteryBox.all()

    @staticmethod
    async def assign_reward_to_box(box_id: int, reward_id: int):
        box = await MysteryBox.get(id=box_id)
        reward = await Rewards.get(id=reward_id)
        if not box or not reward:
            raise ValueError("Mystery Box or Reward not found!")

        await box.rewards.add(reward)

    @staticmethod
    async def get_rewards_for_box(box_id: int):
        box = await MysteryBox.get(id=box_id)
        if not box:
            raise ValueError(f"Mystery Box '{box_id}' not found!")
        return await box.rewards.all()

    @staticmethod
    async def save_member(user_id: int, last_daily: datetime, daily_limit: int):
        await Users.update_or_create(
            user_id=user_id,
            defaults={
                "user_id": user_id,
                "last_daily": last_daily,
                "daily_limit": daily_limit
            }
        )

    @staticmethod
    async def load_member(user_id: int):
        user = await Users.get_or_none(user_id=user_id)
        return user.last_daily if user else None

    @staticmethod
    async def load_all_members():
        users = await Users.all()
        members = {}
        for user in users:
            members[user.user_id] = {
                "last_daily": user.last_daily,
                "daily_limit": user.daily_limit
            }
        return members

    @staticmethod
    async def record_lootbox_opening(user_id: int, lootbox_reward: str):
        await MysteryBoxHistory.create(
            user_id=user_id,
            lootbox_reward=lootbox_reward
        )

    @staticmethod
    async def reset_last_daily():
        await Users.all().update(last_daily=None)

