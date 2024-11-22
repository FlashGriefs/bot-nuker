import aiohttp
import asyncio

async def spam_webhooks(webhooks, message, repeat=1):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for webhook in webhooks:
            if webhook:
                url = webhook["url"]
                for _ in range(repeat):
                    tasks.append(
                        session.post(
                            url,
                            json={"content": message},
                            headers={"Content-Type": "application/json"}
                        )
                    )
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for response, webhook in zip(responses, webhooks * repeat):
            if isinstance(response, aiohttp.ClientResponse) and response.status == 204:
                print(f"Sent message to webhook: {webhook['url']}")
            elif isinstance(response, aiohttp.ClientResponse):
                error_text = await response.text()
                print(f"Failed to send message to webhook {webhook['url']}: {response.status}, {error_text}")
            elif isinstance(response, Exception):
                print(f"Exception occurred for webhook {webhook['url']}: {response}")
