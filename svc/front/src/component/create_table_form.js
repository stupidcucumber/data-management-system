import React, { useState } from "react";
import axios from "axios";

function CreateTableForm({ database_name, onCreate }) {
  const [tableName, setTableName] = useState("");
  const [fields, setFields] = useState([{ field_name: "", field_type: "string" }]);

  const fieldTypes = ["string", "char", "integer", "real", "date", "dateInvl"];

  // Add a new field
  const handleAddField = () => {
    setFields([...fields, { field_name: "", field_type: "string" }]);
  };

  // Remove a field
  const handleRemoveField = (index) => {
    const updatedFields = [...fields];
    updatedFields.splice(index, 1);
    setFields(updatedFields);
  };

  // Update a field's name or type
  const handleFieldChange = (index, fieldName, value) => {
    const updatedFields = [...fields];
    updatedFields[index][fieldName] = value;
    setFields(updatedFields);
  };

  // Handle form submission
  const handleSubmit = (event) => {
    event.preventDefault();
    if (tableName.trim() === "" || fields.length === 0) {
      alert("Please provide a table name and at least one field.");
      return;
    }

    const payload = {
        database_name: database_name,
        table_name: tableName,
        table_fields: fields,
    };

    console.log("Submitting form with payload:", payload);

    // Call API or parent function to create the table
    // Example POST request (replace URL with your actual endpoint):
    axios.post(
        `http://localhost:8000/database/table`,
        payload,
        {
            headers: {
                "Content-Type": "application/json",
            }
        }
    ).then((response) => {
        if (response.status === 200) {
          alert("Table created successfully!");
          if (onCreate) onCreate(); // Notify parent component if needed
        } else {
            console.log(response)
            alert("Error creating table.");
        }
      })
      .catch((error) => console.error("Error:", error));
  };

  return (
    <form className="container mt-4" onSubmit={handleSubmit}>
      <h4>Create Table in Database: {database_name}</h4>

      {/* Table Name Input */}
      <div className="mb-3">
        <label htmlFor="tableName" className="form-label">
          Table Name
        </label>
        <input
          type="text"
          id="tableName"
          className="form-control"
          value={tableName}
          onChange={(e) => setTableName(e.target.value)}
          required
        />
      </div>

      {/* Fields Section */}
      <h5>Fields</h5>
      {fields.map((field, index) => (
        <div key={index} className="row g-3 align-items-end mb-2">
          {/* Field Name */}
          <div className="col">
            <label htmlFor={`field-name-${index}`} className="form-label">
              Field Name
            </label>
            <input
              type="text"
              id={`field-name-${index}`}
              className="form-control"
              value={field.name}
              onChange={(e) =>
                handleFieldChange(index, "field_name", e.target.value)
              }
              required
            />
          </div>

          {/* Field Type */}
          <div className="col">
            <label htmlFor={`field-type-${index}`} className="form-label">
              Field Type
            </label>
            <select
              id={`field-type-${index}`}
              className="form-select"
              value={field.type}
              onChange={(e) =>
                handleFieldChange(index, "field_type", e.target.value)
              }
            >
              {fieldTypes.map((type) => (
                <option key={type} value={type}>
                  {type}
                </option>
              ))}
            </select>
          </div>

          {/* Remove Field Button */}
          <div className="col-auto">
            <button
              type="button"
              className="btn btn-danger"
              onClick={() => handleRemoveField(index)}
              disabled={fields.length === 1} // Prevent removing the last field
            >
              Remove
            </button>
          </div>
        </div>
      ))}

      {/* Add Field Button */}
      <button
        type="button"
        className="btn btn-secondary mb-3"
        onClick={handleAddField}
      >
        Add Field
      </button>

      {/* Submit Button */}
      <button type="submit" className="btn btn-primary">
        Create Table
      </button>
    </form>
  );
}

export default CreateTableForm;
