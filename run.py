#!/usr/bin/env python3
from pottato import init_app
import uvicorn


server = init_app()

if __name__ == "__main__":
    uvicorn.run("run:server", reload=True)
