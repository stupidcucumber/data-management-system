import React, { useState, useEffect } from "react";
import axios from "axios";
import CreateTableForm from "./create_table_form";
import Table from "./table";
import AddTableRow from "./create_table_row";
import EditTableRow from "./edit_table_row";


function DatabaseComponent({ database_name }) {
    const [tables, setTables] = useState([]);
    const [activeTable, setActiveTable] = useState(null);
    const [tableData, setTableData] = useState([]);
    const [activeEditItem, setActiveEditItem] = useState(null);
    const [isModalCreateTableOpen, setIsModalCreateTableOpen] = useState(false);
    const [isModalEditItemOpen, setIsModalEditItemOpen] = useState(false);
    const [isModalCreateItemOpen, setIsModalCreateItemOpen] = useState(false);

    // Fetch database tables on load
    useEffect(() => {
        fetchTables();
    }, [database_name]);

    const fetchTables = () => {
        axios
            .get(`http://localhost:8000/database/${database_name}/table`)
            .then(
                (response) => {
                    console.log("Received the followind data: ", response.data)

                    const tableList = response.data || [];

                    setTables(tableList);
                }
            )
            .catch((error) => console.error("Error fetching tables:", error));
    };

    const fetchItems = () => {

        if (activeTable === null) return;

        axios
            .get(`http://localhost:8000/database/${database_name}/table/${activeTable._id}/item`)
            .then((response) => {
                console.log("Received items: ", response.data);
                setTableData(response.data || []);
            })
            .catch((error) => console.error("Error fetching table content:", error));
    }

    const handleTableClick = (table) => {
        console.log("Table clicked: ", table);
        setActiveTable(table);
        fetchItems();
    };

    const handleRowClick = (item) => {
        console.log(`Edit Row: ${item} in Table: ${activeTable}`);
        setIsModalEditItemOpen(true);
        setActiveEditItem(item);
    };

    const handleTableCreated = () => {
        setIsModalCreateTableOpen(false); // Close modal
        fetchTables(); // Refresh table list after creation
    };

    const handleRowCreated = () => {
        setIsModalCreateItemOpen(false);
        fetchItems()
    }

    const handleTableDelete = () => {
        axios
            .delete(`http://localhost:8000/database/${database_name}/table/${activeTable._id}`)
            .then(
                (response) => {
                    if (response.status === 200) {
                        setTableData([]);
                        setActiveTable(null);
                    }
                }
            )
            .catch(
                (error) => console.error("Error while removing table: ", error)
            )
        fetchTables()
    }

    return (
        <div className="container mt-4">
            <h3 className="mb-4">Database: {database_name}</h3>

            {/* Delete Database Button */}
            <button className="btn btn-danger mb-3">Delete Database</button>

            {/* Table Tabs */}
            <ul className="nav nav-tabs mb-3">
                {
                    tables.map(
                        (table) => (
                            <li className="nav-item" key={table._id}>
                                <button
                                    className={`nav-link ${table === activeTable ? "active" : ""}`}
                                    onClick={() => handleTableClick(table)}
                                >
                                    {table.table_name}
                                </button>
                            </li>
                        )
                    )
                }
                {
                    tables.length === 0 && (
                        <li className="nav-item">
                            <button className="nav-link active" disabled>
                                No Tables Available
                            </button>
                        </li>
                    )
                }
            </ul>

            {/* Create Table Button */}
            <button
                className="btn btn-success mb-3"
                onClick={() => setIsModalCreateTableOpen(true)} // Open modal
            >
                Create Table
            </button>

            {/* Table Content */}
            <div className="table-responsive" style={{ maxHeight: "300px", overflowY: "scroll" }}>
                {
                    activeTable !== null ? (
                        <Table
                            cols={activeTable.table_fields.map((tableField) => tableField.field_name)}
                            items={tableData}
                            onRowClick={handleRowClick}
                        />
                    ) : (
                        <table className="table table-striped table-hover">
                            <thead className="thead-light">
                                <tr>
                                    <th>No Data Available</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr>
                                    <td>No tables found in the database. Create a table to get started.</td>
                                </tr>
                            </tbody>
                        </table>
                    )
                }
            </div>

            {/* Delete Table and Create Item Button */}
            {
                activeTable && tables.length > 0 && (
                    <div>
                        <button
                            className="btn btn-danger mt-3"
                            onClick={handleTableDelete}
                        >
                            Delete Table
                        </button>

                        <button
                            className="btn btn-success mt-3"
                            onClick={
                                () => {
                                    setIsModalCreateItemOpen(true)
                                }
                            }
                        >
                            Add Item
                        </button>
                    </div>
                )
            }

            {/* Create Table Modal */}
            {
                isModalCreateTableOpen && (
                    <div
                    className="modal fade show"
                    style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
                    tabIndex="-1"
                    role="dialog"
                    >
                        <div className="modal-dialog" role="document">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title">Create Table</h5>
                                    <button
                                    type="button"
                                    className="btn-close"
                                    onClick={() => setIsModalCreateTableOpen(false)} // Close modal
                                    aria-label="Close"
                                    ></button>
                                </div>
                                <div className="modal-body">
                                    <CreateTableForm
                                        database_name={database_name}
                                        onCreate={handleTableCreated}
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }


            {/* Create item Modal */}
            {
                isModalCreateItemOpen && (

                    <div
                    className="modal fade show"
                    style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
                    tabIndex="-1"
                    role="dialog"
                    >
                        <div className="modal-dialog" role="document">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title">Create item</h5>
                                    <button
                                    type="button"
                                    className="btn-close"
                                    onClick={() => setIsModalCreateItemOpen(false)} // Close modal
                                    aria-label="Close"
                                    ></button>
                                </div>
                                <div className="modal-body">
                                    <AddTableRow
                                        database_name={database_name}
                                        table_id={activeTable._id}
                                        table_name={activeTable.table_name}
                                        fields={activeTable.table_fields}
                                        onClose={
                                            () => {
                                                setIsModalCreateItemOpen(false);
                                            }
                                        }
                                        onAdd={
                                            () => {
                                                handleRowCreated()
                                            }
                                        }
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }

            {/* Create item Modal */}
            {
                isModalEditItemOpen && (

                    <div
                    className="modal fade show"
                    style={{ display: "block", backgroundColor: "rgba(0, 0, 0, 0.5)" }}
                    tabIndex="-1"
                    role="dialog"
                    >
                        <div className="modal-dialog" role="document">
                            <div className="modal-content">
                                <div className="modal-header">
                                    <h5 className="modal-title">Edit item</h5>
                                    <button
                                    type="button"
                                    className="btn-close"
                                    onClick={
                                        () => {
                                            setActiveEditItem(null);
                                            setIsModalEditItemOpen(false);
                                        }
                                    } // Close modal
                                    aria-label="Close"
                                    ></button>
                                </div>
                                <div className="modal-body">
                                    <EditTableRow
                                        table_name={activeTable.table_name}
                                        item={activeEditItem}
                                        onClose={
                                            () => {
                                                setActiveEditItem(null);
                                                setIsModalEditItemOpen(false);
                                            }
                                        }
                                        onUpdate={
                                            () => {
                                                setActiveEditItem(null);
                                                fetchItems();
                                            }
                                        }
                                    />
                                </div>
                            </div>
                        </div>
                    </div>
                )
            }
        </div>
    );
}

export default DatabaseComponent;
