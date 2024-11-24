import os
from typing import Literal, Optional

from dotenv import load_dotenv
from pymongo import AsyncMongoClient, MongoClient
from pymongo.server_api import ServerApi

load_dotenv()


def get_mongodb_client(uri: Optional[str] = None) -> MongoClient:
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


def get_async_mongodb_client(uri: Optional[str] = None) -> AsyncMongoClient:
    """Create a new asynchronouse client to connect to the MongoDB cluster.

    Parameters
    ----------
    uri : Optional[str]
        URI that leads to the MongoDB cluster.

    Returns
    -------
    AsyncMongoClient
        Client to connect to MongoDB.
    """
    if not uri:
        uri = os.getenv("MONGO_DB_URI")
    return AsyncMongoClient(uri, server_api=ServerApi("1"))


async def check_connection(
    mongodb_client: AsyncMongoClient,
) -> Literal["healthy", "sick"]:
    """Check connection with the MongoDB cluster.

    Parameters
    ----------
    mongodb_client : AsyncMongoClient
        Client to check connection to the MongoDB cluster with.

    Returns
    -------
    Literal["healthy", "sick"]
        Returns "healthy" if connection is successful, otherwise
        returns sick.
    """
    result = "healthy"

    try:
        await mongodb_client.admin.command("ping")
    except Exception:
        result = "sick"

    return result
