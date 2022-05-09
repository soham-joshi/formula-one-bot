import asyncio

def async_wrapper(coro):
    """
    Runs the test case as a coroutine in a new event loop. Use as decorator to the test function.
    """
    def wrapper(*args, **kwargs):
        loop = asyncio.new_event_loop()
        return loop.run_until_complete(coro(*args, **kwargs))
    return wrapper