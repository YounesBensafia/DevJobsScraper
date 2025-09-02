import os
import discord
import dotenv

dotenv.load_dotenv()

intents = discord.Intents.default()
intents.message_content = True


async def send_dm(message: str):
    """Send a DM to the configured USER_ID."""
    token = os.getenv("DISCORD_TOKEN")
    user_id = int(os.getenv("USER_ID"))

    client = discord.Client(intents=intents)

    @client.event
    async def on_ready():
        print(f"Logged in as {client.user}")
        try:
            user = await client.fetch_user(user_id)
            if user:
                await user.send(message)
                print("Message sent successfully")
            else:
                print("User not found")
        except Exception as e:
            print(f"Error: {e}")

        await client.close()

    client.run(token)
