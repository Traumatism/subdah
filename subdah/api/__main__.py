from fastapi import FastAPI
from functools import lru_cache

from ..scanner import Scanner

(app := FastAPI()).get("/subdomains/{domain}")(lru_cache(maxsize=128)(lambda domain: list(map(lambda x: x.as_json(), Scanner(domain).scan()))))

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,  # type: ignore
        host="0.0.0.0",
        port=8000,
    )
