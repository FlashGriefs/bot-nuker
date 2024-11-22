import aiohttp
import asyncio

async def ban_all(token, guild_id, delete_message_seconds=0):
    async with aiohttp.ClientSession() as session:
        headers = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }
        url_members = f"https://discord.com/api/v9/guilds/{guild_id}/members"
        url_bulk_ban = f"https://discord.com/api/v9/guilds/{guild_id}/bulk-ban"

        user_ids = []
        params = {"limit": 1000}
        while True:
            response = await session.get(url_members, headers=headers, params=params)
            if response.status == 200:
                members = await response.json()
                if not members:
                    break
                user_ids.extend(member["user"]["id"] for member in members)
                params["after"] = members[-1]["user"]["id"]
            else:
                error_text = await response.text()
                print(f"Failed to fetch members: {response.status}, {error_text}")
                return None

        tasks = []
        for i in range(0, len(user_ids), 1000):
            batch = user_ids[i:i + 1000]
            payload = {
                "user_ids": batch,
                "delete_message_seconds": delete_message_seconds
            }
            tasks.append(session.post(url_bulk_ban, json=payload, headers=headers))

        responses = await asyncio.gather(*tasks, return_exceptions=True)

        results = {"banned_users": [], "failed_users": []}
        for response in responses:
            if isinstance(response, aiohttp.ClientResponse) and response.status == 200:
                data = await response.json()
                results["banned_users"].extend(data.get("banned_users", []))
                results["failed_users"].extend(data.get("failed_users", []))
            elif isinstance(response, aiohttp.ClientResponse):
                error_text = await response.text()
                print(f"Failed to ban batch: {response.status}, {error_text}")
            elif isinstance(response, Exception):
                print(f"Exception occurred: {response}")

        print(f"Total Banned: {len(results['banned_users'])}")
        print(f"Failed to Ban: {len(results['failed_users'])}")
        return results
