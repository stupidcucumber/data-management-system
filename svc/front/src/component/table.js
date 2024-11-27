export default function Table({ cols , items , onRowClick}) {
    console.log("Items: ", items)
    return (
        <table className="table table-striped table-hover">
            <thead className="thead-light">
                <tr>
                    {
                        cols.map(
                            (col) => (
                                <th key={col}>{col}</th>
                            )
                        )
                    }
                </tr>
            </thead>
            <tbody>
                {
                    items.map(
                        (tableItem) => (
                            <tr
                                key={tableItem._id}
                                onClick={
                                    () => onRowClick(tableItem)
                                }
                                style={{ cursor: "pointer" }}
                            >
                                {
                                    tableItem.items.map(
                                        (column) => (
                                            column.field_type === "dateInvl"
                                            ? <td>{column.field_value.start_date} {column.field_value.end_date}</td>
                                            : <td>{column.field_value}</td>
                                        )
                                    )
                                }
                            </tr>
                        )
                    )
                }
            </tbody>
        </table>
    )
}
