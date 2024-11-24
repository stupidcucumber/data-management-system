import os
from typing import Literal, Optional

from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


def get_database_client(uri: Optional[str] = None) -> MongoClient:
    """Create a new client to connect to the MongoDB cluster.

    Parameters
    ----------
    uri : Optional[str]
        URI that leads to the MongoDB cluster.

    Returns
    -------
    MongoClient
        Client to connect to MongoDB.
    """
    if not uri:
        uri = os.getenv("MONGO_DB_URI")
    return MongoClient(uri, server_api=ServerApi("1"))


def check_connection(uri: Optional[str] = None) -> Literal["healthy", "sick"]:
    """Check connection with the MongoDB cluster.

    Parameters
    ----------
    uri : Optional[str]
        URI leading to the MongoDB cluster.

    Returns
    -------
    Literal["healthy", "sick"]
        Returns "healthy" if connection is successful, otherwise
        returns sick.
    """
    mongodb_client = get_database_client(uri=uri)
    result = "healthy"

    try:
        mongodb_client.admin.command("ping")
    except Exception:
        result = "sick"

    return result
