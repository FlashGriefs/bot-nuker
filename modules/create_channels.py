import aiohttp
import asyncio

async def create_channels(bot_token, guild_id, base_channel_name, num_channels):
    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
        headers = {
            "Authorization": f"Bot {bot_token}",
            "Content-Type": "application/json"
        }
        tasks = [
            session.post(
                url,
                json={"name": f"{base_channel_name}-{i+1}", "type": 0},
                headers=headers
            )
            for i in range(num_channels)
        ]
        responses = await asyncio.gather(*tasks)

        created_channels = []
        for response in responses:
            if response.status in {200, 201}:
                channel = await response.json()
                print(f"Created channel: {channel['id']}")
                created_channels.append(channel)
            else:
                print(f"Failed to create channel: {response.status}")
                created_channels.append(None)
        return created_channels
