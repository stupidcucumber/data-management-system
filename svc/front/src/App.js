import React, { useState, useEffect } from 'react';
import axios from 'axios';
import 'bootstrap/dist/css/bootstrap.min.css';


const App = () => {
    const [databases, setDatabases] = useState([]);
    const [content, setContent] = useState('Welcome! Click a button to view database details.');

    // Fetch databases from the API
    const fetchDatabases = async () => {
        try {
            const response = await axios.get(
                'http://' + process.env.SERVER_HOST + ':' + process.env.SERVER_PORT + '/database'
            );
            setDatabases(response.data); // Assuming response.data is an array of database names
        } catch (error) {
            console.error('Error fetching databases:', error);
            setContent('Failed to load databases. Please try again.');
        }
    };

    // Load databases on component mount
    useEffect(() => {
      fetchDatabases();
    }, []);

    const handleCreateDatabase = () => {
        alert('Database created!');
        // Add your logic for database creation here.
    };

    return (
        <div className="container-fluid">
        <div className="row vh-100">
            {/* Sidebar */}
            <div className="col-3 bg-light border-end d-flex flex-column">
            <div className="p-3">
                <h5>Databases</h5>
                    <div className="list-group">
                    {databases.length > 0 ? (
                        databases.map((db, index) => (
                        <button
                            key={index}
                            className="list-group-item list-group-item-action"
                            onClick={() => setContent(`Details for database: ${db}`)}
                        >
                            {db}
                        </button>
                        ))
                    ) : (
                        <p>There is no databases yet.</p>
                    )}
                    </div>
            </div>
            <div className="mt-auto p-3">
                <button
                className="btn btn-primary w-100"
                onClick={handleCreateDatabase}
                >
                Create Database
                </button>
            </div>
            </div>

            {/* Main Content */}
            <div className="col-9 d-flex justify-content-center align-items-center">
            <div className="text-center">
                <h3>{content}</h3>
            </div>
            </div>
        </div>
        </div>
    );
};

export default App;
