import asyncio


async def maybe_await(function, *args, **kwargs):
    if asyncio.iscoroutinefunction(function):
        return await function(*args, **kwargs)
    else:
        return function(*args, **kwargs)
