from typing import Literal

from fastapi import FastAPI, HTTPException
from src.db.client import check_connection, get_async_mongodb_client
from src.db.database import get_database
from src.db.table import create_table
from src.types import Table, TableItem

app = FastAPI()
mongodb_client = get_async_mongodb_client()


@app.get("/")
async def get_health_status() -> dict[str, Literal["healthy", "sick"]]:
    """Check health of the DMS application.

    Returns
    -------
    dict[str, Literal["healthy", "sick"]]
        Result of checking all vital components of the service.
    """
    return {"database_status": await check_connection(mongodb_client=mongodb_client)}


@app.get("/database")
async def get_databases() -> list[str]:
    """Get all databases or a specific one.

    Returns
    -------
    list[str]
        Names of the existing databases.
    """
    return [
        db_name
        for db_name in await mongodb_client.list_database_names()
        if db_name not in ["local", "admin"]
    ]


@app.delete("/database")
async def delete_database(database_name: str) -> str:
    """Delete database from the MongoDB cluster.

    Parameters
    ----------
    database_name : str
        Name of the database.

    Returns
    -------
    str
        Name of the deleted database.

    Raises
    ------
    HTTPException
        If database does not exist.
    """
    if database_name in await mongodb_client.list_database_names():
        await mongodb_client.drop_database(database_name)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Database with name {database_name} does not exist!",
        )
    return database_name


@app.get("/database/table")
async def get_tables(database_name: str) -> list[Table]:
    """Get all tables in the database.

    Parameters
    ----------
    database_name : str
        Name of the database to extract tables from.

    Returns
    -------
    list[Table]
        List of all tables in the requested database.
    """
    result: list[Table] = []

    database = await get_database(
        database_name=database_name, mongodb_client=mongodb_client
    )

    async for table in database.get_collection("tables").find():
        result.append(Table(**table))

    return result


@app.post("/database/table")
async def post_table(table: Table) -> str:
    """Post new table into the database.

    Parameters
    ----------
    table : Table
        Tables instance that must be inserted.

    Returns
    -------
    str
        Id of the incerted table.
    """
    database = await get_database(
        database_name=table.database_name,
        mongodb_client=mongodb_client,
        not_exist_ok=True,
    )

    collection = database.get_collection("tables")
    result = await collection.insert_one(table.model_dump())
    await create_table(table.table_name, mongodb_client)

    return str(result.inserted_id)


@app.delete("/database/table")
async def delete_table(table: Table) -> str:
    """Delete table from the database.

    Parameters
    ----------
    table : Table
        Table instance to be removed.

    Returns
    -------
    str
        Id of the removed table.
    """
    database = await get_database(
        database_name=table.database_name, mongodb_client=mongodb_client
    )

    collection = database.get_collection("tables")

    await collection.delete_one({"_id": table.id})
    await database.drop_collection(table.table_name)

    return table


@app.get("/table")
async def get_table_items(table: Table) -> list[TableItem]:
    """Get entries in the table.

    Parameters
    ----------
    table : Table
        Table from where to get all items.

    Returns
    -------
    list[TableItem]
        List of items in the table.
    """
    result: list[TableItem] = []
    database = await get_database(table.database_name, mongodb_client=mongodb_client)

    async for table_item in database.get_collection(table.table_name).find():
        result.append(TableItem(**table_item))

    return result


@app.post("/table")
async def post_table_item(table: Table, table_item: TableItem) -> str:
    """Post item into the table.

    Parameters
    ----------
    table : Table
        Table from where item needs to be inserted.
    table_item : TableItem
        Table item to insert.

    Returns
    -------
    str
        Id of the inserted item.
    """
    database = await get_database(table.database_name, mongodb_client=mongodb_client)
    collection = database.get_collection(table.table_name)
    result = await collection.insert_one(table_item.model_dump())
    return str(result.inserted_id)


@app.put("/table")
async def put_table_item(table: Table, table_item: TableItem) -> str:
    """Put item into the table.

    Parameters
    ----------
    table : Table
        Table from where item needs to be updated.
    table_item : TableItem
        Table item to update.

    Returns
    -------
    str
        Id of the updated item.
    """
    database = await get_database(table.database_name, mongodb_client=mongodb_client)
    collection = database.get_collection(table.table_name)

    await collection.update_one(
        filter={"_id": table_item.id},
        update={"$set": table_item.model_dump(exclude=["id"])},
    )

    return str(table_item.id)


@app.delete("/table")
async def delete_table_item(table: Table, table_item: TableItem) -> str:
    """Delete item from the table.

    Parameters
    ----------
    table : Table
        Table from where item needs to be removed.
    table_item : TableItem
        Table item to remove.

    Returns
    -------
    str
        Id of the deleted item.
    """
    database = await get_database(table.database_name, mongodb_client=mongodb_client)
    collection = database.get_collection(table.table_name)

    await collection.delete_one({"_id": table_item.id})

    return str(table_item.id)
