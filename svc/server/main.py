from typing import Literal

from fastapi import FastAPI
from src.db.client import check_connection, get_database_client

app = FastAPI()
mongodb_client = get_database_client()


@app.get("/")
def get_health_status() -> dict[str, Literal["healthy", "sick"]]:
    """Check health of the DMS application.

    Returns
    -------
    dict[str, Literal["healthy", "sick"]]
        Result of checking all vital components of the service.
    """
    return {"database_status": check_connection()}
