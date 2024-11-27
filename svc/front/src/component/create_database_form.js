import React, { useState } from 'react';
import axios from 'axios';

const DatabaseForm = () => {
  const [dbName, setDbName] = useState('');
  const [error, setError] = useState('');

  const handleInputChange = (e) => {
    setDbName(e.target.value);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    // Basic validation
    if (!dbName.trim()) {
      setError('Database name is required');
      return;
    }

    try {
        const response = await axios.post(
            'http://localhost:8000/database',
            {
                database_name: dbName,
                table_names: []
            },
            {
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        );
      if (response.status === 200) {
        alert('Database created successfully!');
        setDbName(''); // Clear input field after successful submission
      }
    } catch (error) {
      setError('Failed to create database');
      console.error(error);
    }
  };

  return (
    <div className="container mt-4">
      <h2>Create a New Database</h2>
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label htmlFor="dbName" className="form-label">Database Name</label>
          <input
            type="text"
            className="form-control"
            id="dbName"
            value={dbName}
            onChange={handleInputChange}
            placeholder="Enter database name"
          />
        </div>

        {error && <div className="alert alert-danger">{error}</div>}

        <button type="submit" className="btn btn-primary float-end">Create</button>
      </form>
    </div>
  );
};

export default DatabaseForm;
