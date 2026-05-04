"""
Concurrency: Async/Await
"""

import asyncio


# Basic async function
async def say_after(delay: float, message: str):
    await asyncio.sleep(delay)
    print(message)


async def main():
    print("Starting...")
    await say_after(1, "Hello")
    await say_after(2, "World")
    print("Done!")


# Run: asyncio.run(main())


# Concurrent tasks with gather
async def fetch_data(id: int) -> dict:
    await asyncio.sleep(1)
    return {"id": id, "data": f"Data for {id}"}


async def gather_all():
    # Run multiple coroutines concurrently
    tasks = [fetch_data(i) for i in range(5)]
    results = await asyncio.gather(*tasks)
    return results


# Sequential vs concurrent timing
async def sequential():
    start = asyncio.get_event_loop().time()
    await fetch_data(1)
    await fetch_data(2)
    await fetch_data(3)
    return asyncio.get_event_loop().time() - start


async def concurrent():
    start = asyncio.get_event_loop().time()
    await asyncio.gather(fetch_data(1), fetch_data(2), fetch_data(3))
    return asyncio.get_event_loop().time() - start


# async for (async iterator)
async def async_generator():
    for i in range(5):
        await asyncio.sleep(0.1)
        yield i


async def consume_async_gen():
    async for value in async_generator():
        print(f"Got: {value}")


# Async context manager
class AsyncResource:
    async def __aenter__(self):
        print("Acquiring resource")
        await asyncio.sleep(0.1)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("Releasing resource")
        await asyncio.sleep(0.1)


async def use_resource():
    async with AsyncResource() as resource:
        print("Using resource")


# Async queue
async def producer(queue: asyncio.Queue):
    for i in range(5):
        await queue.put(i)
        print(f"Produced: {i}")


async def consumer(queue: asyncio.Queue):
    while True:
        item = await queue.get()
        print(f"Consumed: {item}")
        if item == 4:
            break


async def queue_demo():
    queue = asyncio.Queue()
    await asyncio.gather(
        producer(queue),
        consumer(queue)
    )


# Run all demos
if __name__ == "__main__":
    asyncio.run(queue_demo())