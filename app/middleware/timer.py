import time
from fastapi import Request


# Middleware to measure and expose request processing time.
# This function follows FastAPI/Starlette middleware signature:
#   async def middleware(request, call_next)
# where `call_next` is a callable that receives the request and
# returns a Response after further processing (route handler, other
# middleware, etc.).
async def timing_middleware(request: Request, call_next):
    # Record a high-resolution start timestamp before processing.
    # time.perf_counter() is preferred for measuring elapsed time.
    start = time.perf_counter()

    # Call the next component in the ASGI app chain and await the response.
    # This will execute the endpoint and any downstream middleware.
    response = await call_next(request)

    # Compute elapsed time and set a custom response header so clients
    # (or logging) can see how long the request took to process.
    # The value is formatted to 4 decimal places and suffixed with 's'.
    response.headers["X-Process-Time"] = f"{time.perf_counter() - start:.4f}s"

    # Return the response to be sent back to the client.
    return response