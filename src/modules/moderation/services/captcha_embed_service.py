import discord


class CaptchaEmbedService:
    @staticmethod
    async def create_embed(
        title: str, description: str, color: discord.Color, image_url: str = None
    ):
        """
        Creates a general embed with the provided title, description, color, and optional image.
        """
        embed = discord.Embed(title=title, description=description, color=color)
        if image_url:
            embed.set_image(url=image_url)
        return embed

    async def create_welcome_embed(self):
        """
        Creates the welcome embed with the verification instructions.
        """
        return await self.create_embed(
            title="Welcome",
            description="""  
                    In order to get full access to the server, you must complete the following verification process.  

                    Click on `Verify` to get started.  
                    Click on `FAQ` to learn more.
                    """,
            color=discord.Color.blue(),
        )

    async def create_verification_embed(self, captcha_image_url: str):
        """
        Creates the verification embed with the captcha image.
        """
        return await self.create_embed(
            title="Step 3: Confirm You're Human",
            description="""
                    To continue, please verify that you’re human.
                    
                    Enter the numbers from the captcha image below using the numpad. 
                    """,
            color=discord.Color.blue(),
            image_url=captcha_image_url,
        )

    async def create_faq_embed(self):
        """
        Creates the FAQ embed.
        """
        return await self.create_embed(
            title="FAQ",
            description="""  
                    **Why have a verification system?**  
                    A verification system allows communities to enjoy Discord servers without worrying about unsolicited messages, 
                    bad experiences with bot/fake accounts, etc. With this verification process, we minimize exposure to these 
                    inconveniences and ensure a safe environment for everyone.

                    **Can't you just give me the Verified role?**  
                    Manually giving out the Verified role would defeat the purpose of having this verification system, 
                    and communities could be exposed to potential threats. To keep the verification system as efficient as possible, 
                    the team should not be allowed to give any roles to unverified users.

                    **Is this bot safe?**  
                    This bot will never DM you, ask you to bookmark any websites, scan any QR codes, or ask you to provide any personal 
                    information whatsoever.
                    """,
            color=discord.Color.blue(),
        )

    async def create_safety_tips_embed(self):
        """
        Creates the safety tips embed.
        """
        return await self.create_embed(
            title="Step 1: Turn Off DMs",
            description="""
            For your safety, we recommend turning off DMs to protect yourself from:  
            - DM scams  
            - Advertisers  
            - Impersonators  

            How to turn off DMs:  
            1. **Right-click** on this server’s icon  
            2. Click **Privacy Settings**  
            3. Turn off **Direct Messages**  
            4. Click **Done**  

            Once you’ve turned off your DMs, click **Continue** to proceed.
            """,
            color=discord.Color.blue(),
        )

    async def create_rules_embed(self):
        """
        Creates the rules embed.
        """
        return await self.create_embed(
            title="Step 2: Read the Rules ",
            description="""
            Before continuing, you must read and agree to our server rules:  

            - Follow Discord's [Terms of Service](https://discord.com/terms) and [Community Guidelines](https://discord.com/guidelines).  
            - Treat everyone with respect. **Harassment, witch-hunting, sexism, racism, or hate speech** will not be tolerated.  
            - No spam or self-promotion (e.g., server invites, advertisements) **without permission**. This includes DMing server members.  
            - No **age-restricted or obscene content** (e.g., nudity, sexual content, excessive violence, or disturbing imagery).  
            - **"I didn’t know the rules" is not an excuse.** Continuing means you agree to follow them.  

            Click **Continue** if you agree to these rules.
            """,
            color=discord.Color.blue(),
        )

    async def create_captcha_input_embed(self):
        """
        Creates a simple verification embed without a title and image, using only a blue color.
        """
        return await self.create_embed(
            title="", description="```              ```", color=discord.Color.blue()
        )

    async def create_captcha_sucess_embed(self):
        """
        Creates an embed for a successful captcha verification.
        """
        return await self.create_embed(
            title="✅ Captcha Correct!",
            description="You have been verified.",
            color=discord.Color.green(),
        )

    async def create_captcha_invalid_embed(self):
        """
        Creates an embed for an incorrect captcha attempt.
        """
        return await self.create_embed(
            title="❌ Incorrect Captcha",
            description="Please try again.",
            color=discord.Color.red(),
        )
