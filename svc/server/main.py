from typing import Literal

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pymongo.collection import ObjectId
from src.db.client import check_connection, get_async_mongodb_client
from src.db.database import get_database
from src.db.table import create_table, get_table
from src.types import Database, DatabaseName, Table, TableItem

app = FastAPI()
mongodb_client = get_async_mongodb_client()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


@app.post("/database")
async def post_database(database: Database) -> str:
    """Post new database to the MongoDB cluster.

    Parameters
    ----------
    database : Database
        Name of the new database.

    Returns
    -------
    str
        Name of a new database.
    """
    created_database = await get_database(
        database_name=database.database_name,
        mongodb_client=mongodb_client,
        not_exist_ok=True,
    )

    await created_database.create_collection("tables")

    for table in database.table_names:
        await create_table(table, database)

    return database.database_name


@app.delete("/database")
async def delete_database(database_name: DatabaseName) -> str:
    """Delete database from the MongoDB cluster.

    Parameters
    ----------
    database_name : DatabaseName
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
    if database_name.database_name in await mongodb_client.list_database_names():
        await mongodb_client.drop_database(database_name)
    else:
        raise HTTPException(
            status_code=404,
            detail=f"Database with name {database_name.database_name} does not exist!",
        )
    return database_name.database_name


@app.get("/database/{database_name}/table")
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
        database_name=table.database_name, mongodb_client=mongodb_client
    )

    collection = database.get_collection("tables")
    result = await collection.insert_one(table.model_dump())
    await create_table(table.table_name, database)

    return str(result.inserted_id)


@app.delete("/database/{databaseName}/table/{tableId}")
async def delete_table(databaseName: str, tableId: str) -> str:
    """Delete table from the database.

    Parameters
    ----------
    databaseName : str
        Name of the database to delete table from.
    tableId : str
        Id of the table to delete.

    Returns
    -------
    str
        Id of the removed table.
    """
    database = await get_database(
        database_name=databaseName, mongodb_client=mongodb_client
    )

    collection = database.get_collection("tables")

    table = await collection.find_one({"_id": ObjectId(tableId)})

    await collection.delete_one({"_id": ObjectId(tableId)})

    await database.drop_collection(table["table_name"])

    return str(table["_id"])


@app.get("/database/{databaseName}/table/{tableId}/item")
async def get_table_items(databaseName: str, tableId: str) -> list[TableItem]:
    """Get entries in the table.

    Parameters
    ----------
    databaseName : str
        Name of the database.
    tableId : str
        Table from where to get all items.

    Returns
    -------
    list[TableItem]
        List of items in the table.
    """
    result: list[TableItem] = []

    database = await get_database(databaseName, mongodb_client=mongodb_client)

    table = await get_table(tableId=tableId, db=database)

    async for table_item in database.get_collection(table.table_name).find():
        result.append(TableItem(**table_item))

    return result


@app.post("/database/{databaseName}/table/{tableId}/item")
async def post_table_item(
    databaseName: str, tableId: str, table_item: TableItem
) -> str:
    """Post item into the table.

    Parameters
    ----------
    databaseName : str
        Name of the database to post item to.
    tableId : str
        Table from where item needs to be inserted.
    table_item : TableItem
        Table item to insert.

    Returns
    -------
    str
        Id of the inserted item.
    """
    database = await get_database(databaseName, mongodb_client=mongodb_client)

    table = await get_table(tableId, database)

    collection = database.get_collection(table.table_name)

    result = await collection.insert_one(table_item.model_dump())

    return str(result.inserted_id)


@app.put("/database/{databaseName}/table/{tableId}/item")
async def put_table_item(databaseName: str, tableId: str, table_item: TableItem) -> str:
    """Put item into the table.

    Parameters
    ----------
    databaseName : str
        Name of the database to post item to.
    tableId : str
        Table from where item needs to be inserted.
    table_item : TableItem
        Table item to update.

    Returns
    -------
    str
        Id of the updated item.
    """
    database = await get_database(databaseName, mongodb_client=mongodb_client)

    table = await get_table(tableId, database)

    collection = database.get_collection(table.table_name)

    await collection.update_one(
        filter={"_id": ObjectId(table_item.id)},
        update={"$set": table_item.model_dump(exclude=["id"])},
    )

    return str(table_item.id)


@app.delete("/database/{databaseName}/table/{tableId}/item/{itemId}")
async def delete_table_item(databaseName: str, tableId: str, itemId: str) -> str:
    """Delete item from the table.

    Parameters
    ----------
    databaseName : str
        Name of the database to post item to.
    tableId : str
        Table from where item needs to be inserted.
    itemId : str
        Id of the table item to remove.

    Returns
    -------
    str
        Id of the deleted item.
    """
    database = await get_database(databaseName, mongodb_client=mongodb_client)

    table = await get_table(tableId, database)

    collection = database.get_collection(table.table_name)

    await collection.delete_one({"_id": ObjectId(itemId)})

    return itemId
