// Import necessary modules
import React, { useState } from 'react';
import axios from 'axios';
import { Button, Container, Table, Form, Col, Row } from 'react-bootstrap';

function App() {
  // Initialize state variables
  const [fileData, setFileData] = useState(null);
  const [tableData, setTableData] = useState([]);

  // Function to handle file input change
  const onFileChange = (event) => {
    // Update the fileData state with the selected file
    setFileData(event.target.files[0]);
  };

  // Function to handle file upload
  const onFileUpload = () => {
    // Create a new FormData instance
    const formData = new FormData();

    // Append the selected file to the form data
    formData.append('file', fileData);

    // Make a POST request to the server to upload the file
    axios.post("http://localhost:8000/upload-data/", formData).then((response) => {
      console.log(response);
    });
  };

  // Function to fetch data from the server
  const fetchData = () => {
    // Make a GET request to the server to retrieve data
    axios.get("http://localhost:8000/get-data/").then((response) => {
      // Update the tableData state with the received data
      setTableData(response.data);
      console.log(response);
    });
  };

  return (
    <Container className="mt-5">
      <Form>
        <Form.Group as={Row} controlId="formFile" className="mb-3">
          <Form.Label column sm="2">Select CSV File</Form.Label>
          <Col sm="10">
            <Form.Control type="file" onChange={onFileChange} />
          </Col>
        </Form.Group>

        <Button variant="primary" onClick={onFileUpload}>Upload Data</Button>{' '}
        <Button variant="success" onClick={fetchData}>Get Data</Button>
      </Form>
      
      {/* Check if tableData is an array and if it has any items */}
      {Array.isArray(tableData) && tableData.length > 0 && 
        <Table striped bordered hover className="mt-5">
          <thead>
            <tr>
              {/* Render column headers dynamically */}
              {Object.keys(tableData[0]).map((header, index) => (
                <th key={index}>{header}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {/* Render table rows dynamically */}
            {tableData.map((row, index) => (
              <tr key={index}>
                {/* Render cell data dynamically */}
                {Object.values(row).map((value, index) => (
                  <td key={index}>{value}</td>
                ))}
              </tr>
            ))}
          </tbody>
        </Table>
      }
    </Container>
  );
}

// Export the App component as default
export default App;