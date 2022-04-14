import fastapi
import functools

from typing import Dict, List, Optional

from .. import CACHE_SIZE
from ..scanner import Scanner

app = fastapi.FastAPI()


@app.get("/{domain}/subdomains")
@functools.lru_cache(maxsize=CACHE_SIZE)
def _(domain: str) -> List[Dict[str, Optional[str]]]:
    """ Get the subdomains of a domain. """
    return list(
        map(lambda x: x.as_json(), Scanner(domain).scan())
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="subdah.api.__main__:app",  # type: ignore
        host="0.0.0.0",
        port=8000,
        reload=True,
        debug=True
    )
