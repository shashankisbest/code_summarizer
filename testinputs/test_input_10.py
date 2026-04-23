import asyncio
from typing import Coroutine

async def fetch_data(url: str, delay: float = 1) -> str:
    """Simulate fetching data from URL."""
    await asyncio.sleep(delay)
    return f"Data from {url}"

async def process_data(data: str) -> str:
    """Process fetched data."""
    await asyncio.sleep(0.5)
    return data.upper()

async def main():
    """Main async function to fetch and process multiple URLs."""
    urls = ['http://api.example.com/1', 'http://api.example.com/2', 'http://api.example.com/3']
    
    tasks = [fetch_data(url) for url in urls]
    results = await asyncio.gather(*tasks)
    
    processed = [await process_data(result) for result in results]
    return processed

if __name__ == "__main__":
    result = asyncio.run(main())
    print(result)
