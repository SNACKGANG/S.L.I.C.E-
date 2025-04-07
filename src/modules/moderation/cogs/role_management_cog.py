from discord.ext import commands
from ..controllers.role_controller import RoleController


class RoleManagementCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_controller = RoleController()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def add_role_bulk(self, ctx, role_id: int):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith(('.xlsx', '.xls')):
                file_bytes = await attachment.read()
                await self.role_controller.process_roles(ctx, role_id, file_bytes, action="add")
            else:
                await ctx.send("Please attach a valid Excel file (.xlsx or .xls).")
        else:
            await ctx.send("Attach an Excel file.")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def remove_role_bulk(self, ctx, role_id: int):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            if attachment.filename.endswith(('.xlsx', '.xls')):
                file_bytes = await attachment.read()
                await self.role_controller.process_roles(ctx, role_id, file_bytes, action="remove")
            else:
                await ctx.send("Please attach a valid Excel file (.xlsx or .xls).")
        else:
            await ctx.send("Attach an Excel file.")
