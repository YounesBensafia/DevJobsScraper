import discord
import httpx
import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables from parent directory
env_path = Path(__file__).resolve().parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

TOKEN = os.getenv("DISCORD_TOKEN")
API_URL = os.getenv("DISCORD_API_URL")
intents = discord.Intents.default()
intents.guilds = True
intents.messages = True
intents.message_content = True  # Needed to read commands and get message content
client = discord.Client(intents=intents)

TARGET_GUILD_NAME = "قاعدة ارهابية" 
TARGET_CHANNEL_NAME = "khdma-w-draham"   

def format_job_message(job):
    return f"""📢 **{job['title']}**
🏢 Company: {job['company']}
🕒 Posted: {job['time']}
💼 Tags: {job['tags']}
🌍 FROM: {job['locations']}
💰 Salary: {job['currency']}{job['salary_from']} - {job['currency']}{job['salary_to']}
🔗 [Apply Now]({job['link']})
FOR THE QAEIDA (MTKHAFOCH ITS REMOTE JOB) "younes zaeim"
"""

async def fetch_first_job():
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get(API_URL)
            response.raise_for_status()
            jobs = response.json()
            print("✅ Jobs reçus :", jobs)
            return jobs if jobs else None
    except httpx.RequestError as e:
        print(f"❌ Failed to fetch job: {e.request.url if hasattr(e, 'request') else 'Unknown URL'}")
        print(f"🔴 Détail de l’erreur: {e}")
        return None

@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")

    job = await fetch_first_job()
    
    if not job:
        print("❌ No job found in the list.")
        return

    for guild in client.guilds:
        if guild.name == TARGET_GUILD_NAME:
            for channel in guild.text_channels:
                if channel.name == TARGET_CHANNEL_NAME:
                    print(f"📡 Sending job to #{channel.name}")
                    await channel.send(format_job_message(job[7]))
                    return

    print("❌ Server or channel not found.")

client.run(TOKEN)