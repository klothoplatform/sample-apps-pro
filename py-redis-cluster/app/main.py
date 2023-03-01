from uvicorn import Server, Config
import asyncio

import users
import quotes

async def main():
    configs = [
        Config(app=users.app, host="0.0.0.0", port=3000),
        Config(app=quotes.app, host="0.0.0.0", port=3002),
    ]
    servers = [Server(c).serve() for c in configs]
    _, pending = await asyncio.wait(servers, return_when=asyncio.FIRST_COMPLETED)
    
    print("Shutting down")
    for pending_task in pending:
        pending_task.cancel("Another service died, server is shutting down")

if __name__ == "__main__":
    asyncio.run(main())
