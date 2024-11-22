import aiohttp
import asyncio

async def create_webhooks(bot_token, channel_ids, webhook_name):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        tasks = [
            session.post(
                f"https://discord.com/api/v10/channels/{channel_id}/webhooks",
                json={"name": webhook_name},
                headers=headers
            )
            for channel_id in channel_ids
        ]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        webhooks = []
        for response, channel_id in zip(responses, channel_ids):
            if isinstance(response, aiohttp.ClientResponse) and response.status in {200, 201}:
                webhook = await response.json()
                print(f"Created webhook in channel {channel_id}: {webhook['id']}")
                webhooks.append(webhook)
            elif isinstance(response, aiohttp.ClientResponse):
                error_text = await response.text()
                print(f"Failed to create webhook in channel {channel_id}: {response.status}, {error_text}")
                webhooks.append(None)
            elif isinstance(response, Exception):
                print(f"Exception occurred for channel {channel_id}: {response}")
                webhooks.append(None)
        return webhooks
