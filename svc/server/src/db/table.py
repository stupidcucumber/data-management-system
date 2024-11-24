from fastapi import HTTPException
from pymongo.asynchronous.database import AsyncDatabase


async def create_table(table_name: str, db: AsyncDatabase) -> None:
    """Create a new table in the database.

    Parameters
    ----------
    table_name : str
        Name of the table (collection) to create.
    db : AsyncDatabase
        Database where table must be created.

    Raises
    ------
    HTTPException
        If table already exists.
    """
    if table_name in await db.list_collection_names():
        raise HTTPException(
            status_code=422, detail=f"Table with name {table_name} already exists!"
        )
    await db.create_collection(table_name)
