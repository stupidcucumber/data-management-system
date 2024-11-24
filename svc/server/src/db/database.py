from fastapi import HTTPException
from pymongo import AsyncMongoClient
from pymongo.asynchronous.database import AsyncDatabase


async def get_database(
    database_name: str, mongodb_client: AsyncMongoClient, not_exist_ok: bool = False
) -> AsyncDatabase:
    """Get database from the MongoDB cluster.

    Parameters
    ----------
    database_name : str
        Name of the database.
    mongodb_client : AsyncMongoClient
        Client to be used while extracting.
    not_exist_ok : bool
        If database is not present in the cluster error will not be thrown.

    Returns
    -------
    AsyncDatabase
        Database extracted from the cluster.

    Raises
    ------
    HTTPException
        If database does not exist.
    """
    if (
        not not_exist_ok
    ) and database_name not in await mongodb_client.list_database_names():
        raise HTTPException(
            status_code=404,
            detail=f"Database with name {database_name} does not exist!",
        )
    return mongodb_client.get_database(database_name)
