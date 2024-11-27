import axios from "axios";
import React, { useState } from "react";

function AddTableRow({ database_name, table_name, table_id, fields, onClose, onAdd }) {
    const [rowData, setRowData] = useState(() => {
        // Initialize the rowData object with default values based on field types
        const initialState = {};
        fields.forEach(
            (field) => {
                if (field.field_type === "dateInvl") {
                    initialState[field.field_name] = { start_date: "", end_date: "" };
                } else {
                    initialState[field.field_name] = "";
                }
                }
        );
        return initialState;
    });

    const [errors, setErrors] = useState({});

    const validateField = (field, value) => {
        const { type } = field;
        let error = "";

        switch (type) {
            case "integer":
                if (!/^-?\d+$/.test(value)) error = "Must be an integer.";
                break;
            case "string":
                if (typeof value !== "string" || value.trim() === "")
                error = "Must be a string.";
                break;
            case "char":
                if (value.length !== 1) error = "Must be a single character.";
                break;
            case "real":
                if (!/^-?\d+(\.\d+)?$/.test(value)) error = "Must be a real number.";
                break;
            case "date":
                if (isNaN(Date.parse(value))) error = "Must be a valid date.";
                break;
            case "dateInvl":
                const { start_date, end_date } = value;
                if (!start_date || isNaN(Date.parse(start_date)))
                    error = "Start date must be valid.";
                else if (!end_date || isNaN(Date.parse(end_date)))
                    error = "End date must be valid.";
                else if (new Date(start_date) >= new Date(end_date))
                    error = "Start date must be before end date.";
                break;
            default:
                break;
        }

        return error;
    };

    const handleInputChange = (field, value) => {
        const newRowData = { ...rowData };

        if (field.field_type === "dateInvl") {
        // Handle date interval fields
            newRowData[field.field_name] = { ...newRowData[field.field_name], ...value };
        } else {
            newRowData[field.field_name] = value;
        }

        setRowData(newRowData);

        // Validate field
        setErrors({
            ...errors,
            [field.field_name]: validateField(field, newRowData[field.field_name]),
        });
    };

  const handleSubmit = (event) => {
    console.log("Fields", fields)

    console.log("Submitting the following item: ", rowData)

    event.preventDefault();

    // Validate all fields before submission
    const newErrors = {};
    fields.forEach((field) => {
      const error = validateField(field, rowData[field.field_name]);
      if (error) newErrors[field.field_name] = error;
    });

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
        // No validation errors, proceed to submit
        const payload = Object.entries(rowData).map(
            (item, idx) => {
                return {
                    "field_type": fields.filter(
                        (field) => {
                            return field.field_name === item[0]
                        }
                    )[0].field_type,
                    "field_name": item[0],
                    "field_value": item[1]
                };
            }
        )

        console.log("Sanding payload: ", payload)

        axios
            .post(
                `http://localhost:8000/database/${database_name}/table/${table_id}/item`,
                {items: payload},
                {
                    headers: {
                        'Content-Type': 'application/json'
                    }
                }
            )
            .then(
                (response) => {
                    console.log("Response: ", response)
                    if (response.status === 200) {
                        alert("Row added successfully!");
                    if (onAdd) onAdd(); // Notify parent about the addition
                        onClose(); // Close the modal
                    } else {
                        alert("Failed to add row.");
                    }
                }
            )
            .catch(
                (error) => {
                    console.error("Error adding row:", error);
                    alert("An error occurred while adding the row.");
                }
            );
    }
  };

  return (
    <div className="container mt-3">
        <h5>Add Row to Table: {table_name}</h5>
        <form onSubmit={(event) => handleSubmit(event, fields)}>
        {fields.map((field) => (
          <div className="mb-3" key={field.field_name}>
            <label htmlFor={`field-${field.field_name}`} className="form-label">
              {field.field_name} ({field.field_type})
            </label>
            {field.field_type === "dateInvl" ? (
              <>
                <input
                  type="date"
                  id={`field-${field.field_name}-start`}
                  className={`form-control mb-2 ${
                    errors[field.field_name] ? "is-invalid" : ""
                  }`}
                  placeholder="Start Date"
                  value={rowData[field.field_name].start_date}
                  onChange={(e) =>
                    handleInputChange(field, { start_date: e.target.value })
                  }
                />
                <input
                  type="date"
                  id={`field-${field.field_name}-end`}
                  className={`form-control ${
                    errors[field.field_name] ? "is-invalid" : ""
                  }`}
                  placeholder="End Date"
                  value={rowData[field.field_name].end_date}
                  onChange={(e) =>
                    handleInputChange(field, { end_date: e.target.value })
                  }
                />
                {errors[field.field_name] && (
                  <div className="invalid-feedback">{errors[field.field_name]}</div>
                )}
              </>
            ) : (
              <input
                type={
                  field.field_type === "integer"
                    ? "number"
                    : field.field_type === "real"
                    ? "number"
                    : field.field_type === "date"
                    ? "date"
                    : "text"
                }
                id={`field-${field.field_name}`}
                className={`form-control ${
                  errors[field.field_name] ? "is-invalid" : ""
                }`}
                placeholder={`Enter ${field.field_name}`}
                value={rowData[field.field_name]}
                onChange={(e) => handleInputChange(field, e.target.value)}
              />
            )}
            {errors[field.field_name] && (
              <div className="invalid-feedback">{errors[field.field_name]}</div>
            )}
          </div>
        ))}

        <div className="d-flex justify-content-end">
          <button
            type="button"
            className="btn btn-secondary me-2"
            onClick={onClose}
          >
            Cancel
          </button>
          <button type="submit" className="btn btn-primary">
            Add Row
          </button>
        </div>
      </form>
    </div>
  );
}

export default AddTableRow;
