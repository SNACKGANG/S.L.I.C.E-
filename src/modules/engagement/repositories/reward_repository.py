from src.modules.engagement.models.reward_model import Rewards


class RewardRepository:
    @staticmethod
    async def create_reward(name: str, value: str, chance: int, limit: int, color: str, image_url: str, currency_id: int):
        return await Rewards.create(
            name=name, value=value, chance=chance, limit=limit, color=color, image_url=image_url, currency_id=currency_id
        )

    @staticmethod
    async def update_reward(name: str, value: str = None, chance: int = None, limit: int = None, color: str = None,
                            image_url: str = None):
        reward = await Rewards.get(name=name)
        if not reward:
            raise ValueError(f"Reward '{name}' not found!")

        if value is not None:
            reward.value = value
        if chance is not None:
            reward.chance = chance
        if limit is not None:
            reward.limit = limit
        if color is not None:
            reward.color = color
        if image_url is not None:
            reward.image_url = image_url

        await reward.save()
        return reward

    @staticmethod
    async def list_rewards(box_id: int = None):
        if box_id:
            rewards = await Rewards.filter(mystery_box_id=box_id).all()
        else:
            rewards = await Rewards.all()

        return [
            {
                "name": reward.name,
                "value": reward.value,
                "chance": reward.chance,
                "limit": reward.limit,
                "opened_this_month": reward.opened_this_month,
                "color": reward.color,
                "image_url": reward.image_url,
            }
            for reward in rewards
        ]

    @staticmethod
    async def reset_opened_this_month(box_id: int = None):
        if box_id:
            rewards = await Rewards.filter(mystery_box_id=box_id).all()
        else:
            rewards = await Rewards.all()

        for reward in rewards:
            reward.opened_this_month = 0
            await reward.save()

    @staticmethod
    async def get_all_rewards(box_id: int = None):
        if box_id:
            return await Rewards.filter(mystery_box_id=box_id).all()
        return await Rewards.all()

    @staticmethod
    async def get_reward_by_name(name: str):
        return await Rewards.get_or_none(name=name)

    @staticmethod
    async def increment_opened_this_month(reward_id: int):
        reward = await Rewards.get(id=reward_id)
        if reward:
            reward.opened_this_month += 1
            await reward.save()
        return reward

    @staticmethod
    async def get_rewards_by_box(box_id: int):
        return await Rewards.filter(boxes_linked_to_rewards__id=box_id).all()

    @staticmethod
    async def get_chances_by_box(box_id: int):
        rewards = await Rewards.filter(mystery_box_id=box_id).all()
        return [reward.chance for reward in rewards]
