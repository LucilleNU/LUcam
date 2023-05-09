/* eslint-disable jsx-a11y/media-has-caption */
import React, { useEffect, useState } from "react";
import ReactPlayer from "react-player";

function Recordings() {
  const [recordings, setRecordings] = useState([]);
  useEffect(async () => {
    const response = await fetch("http://localhost:5000/recordings", {
      method: "GET",
    });
    const data = await response.json();
    if (data) {
      console.log(data?.data);
      setRecordings(data?.data);
    }
  }, []);

  return (
    <div>
      <div style={{ textAlign: "center", marginTop: "3vh", marginLeft: "10vw" }}>
        <h1>Recordings</h1>
      </div>
      <div
        style={{
          display: "flex",
          marginLeft: "18vw",
          marginTop: "5vh",
          flexDirection: "row",
          justifyContent: "space-around",
        }}
      >
        {recordings !== [] &&
          recordings.map((recording) => (
            <div style={{ boxShadow: "0 0 5px rgb(0,0,0,0.5)", padding: "3px" }}>
              <ReactPlayer url={recording[0]} controls width="30vw" height="fit-content" />
            </div>
          ))}
      </div>
    </div>
  );
}

export default Recordings;
