from ..services.role_service import RoleService


class RoleController:
    def __init__(self):
        self.role_service = RoleService()

    async def process_roles(self, ctx, role_id: int, file_bytes: bytes, action: str):
        if action not in ["add", "remove"]:
            raise ValueError("Invalid action. Use 'add' or 'remove'.")
        await self.role_service.process_roles_from_excel(ctx, role_id, file_bytes, action)
