import aiohttp
import asyncio

async def delete_channels(bot_token, guild_id):
    async with aiohttp.ClientSession() as session:
        url = f"https://discord.com/api/v10/guilds/{guild_id}/channels"
        headers = {"Authorization": f"Bot {bot_token}"}
        response = await session.get(url, headers=headers)
        if response.status == 200:
            channels = await response.json()
            tasks = [
                session.delete(
                    f"https://discord.com/api/v10/channels/{channel['id']}",
                    headers=headers
                )
                for channel in channels
            ]
            responses = await asyncio.gather(*tasks)

            for response, channel in zip(responses, channels):
                if response.status == 204:
                    print(f"Deleted channel: {channel['id']}")
                else:
                    print(f"Failed to delete channel {channel['id']}: {response.status}")
            return [response.status == 204 for response in responses]
        else:
            print(f"Failed to fetch channels: {response.status}")
        return []
