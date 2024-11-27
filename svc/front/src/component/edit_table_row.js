import axios from "axios";
import React, { useState } from "react";

function EditTableRow({ database_name, table_name, item, onClose, onUpdate }) {
    const [rowData, setRowData] = useState(item.items);
    const [isSubmitting, setIsSubmitting] = useState(false);

    // Handle input changes
    const handleInputChange = (idx, value) => {
        const newRowData = [...rowData];
        newRowData[idx].field_value = value;
        setRowData(newRowData);
    };

    // Submit updated row data
    const handleSubmit = (event) => {
        event.preventDefault();
        setIsSubmitting(true);
        axios.post(
            `http://localhost:8000/database/${database_name}/table/${table_name}/item/${item._id}`,

        )
        .then((response) => {
            if (response.status === 200) {
                alert("Row updated successfully!");
                if (onUpdate) onUpdate(); // Notify parent about update
                onClose(); // Close the modal
            } else {
                alert("Failed to update row.");
            }
        })
        .catch((error) => {
            console.error("Error updating row:", error);
            alert("An error occurred while updating the row.");
        })
        .finally(() => setIsSubmitting(false));
    };

    return (
        <div className="container mt-3">
        <h5>Edit Row (ID: {item._id}) in Table: {table_name}</h5>
        <form onSubmit={handleSubmit}>
            {
            rowData.map(
                (item, idx) => (
                    <div className="mb-3" key={item._id}>
                        <label htmlFor={`field-${item._id}`} className="form-label">
                            {item.field_name}
                        </label>
                        <input
                            type="text"
                            id={`field-${item._id}`}
                            className="form-control"
                            value={item.field_value}
                            onChange={(e) => handleInputChange(idx, e.target.value)}
                        />
                    </div>
                )
            )
            }

            <div className="d-flex justify-content-end">
            <button
                type="button"
                className="btn btn-secondary me-2"
                onClick={onClose}
                disabled={isSubmitting}
            >
                Cancel
            </button>
            <button type="submit" className="btn btn-primary" disabled={isSubmitting}>
                {isSubmitting ? "Updating..." : "Save Changes"}
            </button>
            </div>
        </form>
        </div>
    );
}

export default EditTableRow;
