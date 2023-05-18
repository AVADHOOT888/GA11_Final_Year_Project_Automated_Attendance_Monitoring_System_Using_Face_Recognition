import React, { useState } from "react";
import "./FaceRecognition.css";
import Table from "./Table";
import {
  MDBFile,
} from "mdb-react-ui-kit";

function App(props) {
  const [tab, setTab] = useState(0);
  const [selectedFile, setSelectedFile] = useState(null);
  const [dat, setDat] = useState([]);
  const handleLogout = () => {
    props.setDirect(0);
  };

  const handleSubmit = (event) => {
    event.preventDefault();
    const formData = new FormData();
    formData.append("file", selectedFile);

    fetch("http://127.0.0.1:5000/api/upload-image", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((Data) => {
        const dataArray = JSON.parse(Data.data);
        setDat(dataArray);
        setTab(1);
      })
      .catch((error) => {
        console.error(error);
      });

    // setTab(1);
  };

  const handleFileInput = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  return (
    <>
      <nav className="navbar bg-body-tertiary">
        <div className="container-fluid d-flex align-items-center">
          <button
            onClick={handleLogout}
            type="button"
            className="btn btn-danger"
            style={{ visibility: "hidden" }}
          >
            LogOut
          </button>
          <div
            style={{
              color: "white",
              textShadow: "2px 2px 4px #000000",
              fontSize: "60px",
              fontFamily: "Oswald",
            }}
          >
            Attendance Monitoring System
          </div>
          {/* <div className="container d-flex justify-content-end"> */}
          <button
            onClick={handleLogout}
            type="button"
            className="btn btn-danger"
          >
            LogOut
          </button>
          {/* </div> */}
        </div>
      </nav>

      <nav className="navbar bg-body-tertiary" style={{ visibility: "hidden" }}>
        <div className="container-fluid d-flex align-items-center">
          <button
            onClick={handleLogout}
            type="button"
            className="btn btn-danger"
            style={{ visibility: "hidden" }}
          >
            LogOut
          </button>
          <div
            style={{
              color: "white",
              textShadow: "2px 2px 4px #000000",
              fontSize: "30px",
              fontFamily: "Oswald",
            }}
          >
            Attendance Monitoring System
          </div>
          {/* <div className="container d-flex justify-content-end"> */}
          <button
            onClick={handleLogout}
            type="button"
            className="btn btn-danger"
          >
            LogOut
          </button>
          {/* </div> */}
        </div>
      </nav>

      <div
        className="container"
        style={{
          width: "fit-content",
          // padding: "84px 0px 0px 0px",
          // margin: "0px 0px 0px 380px",
        }}
      >
        <div
          className="container d-flex align-items-center flex-column"
          // style={{ margin: "20px 0px 0px 0px", width: "750px" }}
        >
          <div
            style={{
              fontWeight: "bold",
              margin: "20px",
              fontSize: "20px",
              color: "white",
            }}
          >
            Select Image File
          </div>

          <div className="container d-flex bd-highlight mb-3">
            <MDBFile
              onChange={handleFileInput}
              className="p-2 bd-highlight"
              wrapperclassname="mb-4 w-100"
              id="formControlLg"
              type="file"
              size="lg"
            />
            <button
              onClick={handleSubmit}
              style={{ margin: "0px 0px 0px 16px", width: "88px" }}
              className="p-2 bd-highlight btn btn-success"
              type="button"
            >
              Upload
            </button>
          </div>
        </div>

        <div className="container" style={{ width: "1000px" }}>
          {tab === 1 ? (
            
          <Table data={dat} />
          ) : (
            <div>
              <h2 style={{ color: "white" }}>Please upload image</h2>
            </div>
          )}
        </div>
      </div>
    </>
  );
}

export default App;
