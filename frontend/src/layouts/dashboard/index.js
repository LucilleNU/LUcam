/* eslint-disable no-use-before-define */
/* eslint-disable jsx-a11y/label-has-associated-control */
/* eslint-disable no-plusplus */
/* eslint-disable no-restricted-syntax */
/* eslint-disable no-await-in-loop */
/* eslint-disable jsx-a11y/media-has-caption */
/**
=========================================================
* Material Dashboard 2 React - v2.1.0
=========================================================

* Product Page: https://www.creative-tim.com/product/material-dashboard-react
* Copyright 2022 Creative Tim (https://www.creative-tim.com)

Coded by www.creative-tim.com

 =========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
*/
// import Footer from "examples/Footer";

import ComplexStatisticsCard from "examples/Cards";
import Grid from "@mui/material/Grid";

// Material Dashboard 2 React components
import MDBox from "components/MDBox";
// @mui material components

import CalendarMonthIcon from "@mui/icons-material/CalendarMonth";
import AccessTimeIcon from "@mui/icons-material/AccessTime";
import CloudIcon from "@mui/icons-material/Cloud";

import { Modal, Typography, Box } from "@mui/material";

import "./index.css";

// Material Dashboard 2 React components

// Material Dashboard 2 React example components
import DashboardNavbar from "examples/Navbars/DashboardNavbar";
import DashboardLayout from "examples/LayoutContainers/DashboardLayout";
// import Footer from "examples/Footer";

// Data

// Dashboard components
import React, { useEffect, useRef, useState } from "react";
import io from "socket.io-client";
import MDButton from "components/MDButton";
import axios from "axios";
import DateTime from "./data/Datetime";

const CLOUDINARY_API = "https://api.cloudinary.com/v1_1/dq4l61m3h/mh/upload";
const CLOUDINARY_UPLOAD_PRESET = "jzfnfrsi/mh/upload";

function Dashboard() {
  const [detecting, setDetecting] = useState(false);
  const socketRef = useRef(null);

  const myVideo = useRef();
  const myImage = useRef();
  const canvasRef = useRef(null);
  const intervalRef = useRef(null);

  const [displayDate, setDisplayDate] = useState(null);
  const [displayTime, setDisplayTime] = useState(null);
  const [date, setDate] = useState(new Date());

  useEffect(() => {
    const timer = setInterval(() => {
      const currentDate = new Date();
      const options = { day: "numeric", month: "short", year: "numeric" };
      const formattedDate = currentDate.toLocaleDateString("en-US", options);
      const hours = currentDate.getHours().toString().padStart(2, "0");
      const minutes = currentDate.getMinutes().toString().padStart(2, "0");
      const seconds = currentDate.getSeconds().toString().padStart(2, "0");

      setDisplayDate(formattedDate);
      setDisplayTime(`${hours}:${minutes}:${seconds}`);
    }, 1000); // Update every 1 second

    return () => clearInterval(timer); // Cleanup interval on component unmount
  }, []);

  useEffect(() => {
    socketRef.current = io("http://localhost:5000/");
    socketRef.current.on("connect", () => {});

    navigator.mediaDevices
      .getUserMedia({ video: { aspectRatio: 1438 / 578 }, audio: true })
      .then((captured) => {
        myVideo.current.srcObject = captured;
      });

    return () => {
      socketRef.current.off("image");
      socketRef.current.off("processed_image");
      socketRef.current.disconnect();
      clearInterval(intervalRef.current); // Clear the interval when the component is unmounted
    };
  }, []);

  useEffect(() => {
    if (detecting) {
      const canvas = canvasRef.current;
      const context = canvas.getContext("2d");
      const video = myVideo.current;

      intervalRef.current = setInterval(() => {
        const { width } = video;
        const { height } = video;
        context.drawImage(video, 0, 0, width, height);
        const data = canvas.toDataURL("image/jpeg", 0.4);
        context.clearRect(0, 0, width, height);
        if (detecting) socketRef.current.emit("image", data);
      }, 1000 / 30);
      socketRef.current.on("processed_image", (image) => {
        if (myImage.current) myImage.current.setAttribute("src", image);
      });
    } else {
      clearInterval(intervalRef.current); // Clear the interval when detecting is set to false
    }
  }, [detecting]);

  const handleDetect = () => {
    setDetecting(true);
  };

  const handleStopDetect = () => {
    setDetecting(false);
    socketRef.current.emit("merge-processed");
  };

  const toggleNotification = (status) => {
    if (status === "yes") {
      setTimeout(requestNotificationPermission, 1000);
    }

    fetch("http://localhost:5000/toggle_notification", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: `status=${status}&permission=${Notification.permission}`,
    })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw new Error("Login failed");
      })
      .then((jsonData) => {
        console.log(jsonData.message);
        // Handle the successful login message
      })
      .catch((error) => {
        console.error("Error:", error.message);
        // Handle the login failure error
      });
  };

  const requestNotificationPermission = () => {
    if (Notification.permission === "granted") {
      console.log("User has already allowed notifications");
    } else if (Notification.permission !== "denied") {
      // Show a popup message asking the user if they want to allow notifications
      setOpen(true);
    } else {
      console.log("User has denied notifications");
    }
  };

  const [selectedOption, setSelectedOption] = useState("no");
  const [open, setOpen] = useState(false);

  const handleOptionChange = (event) => {
    setSelectedOption(event.target.value);
    toggleNotification(event.target.value);
  };

  const handleAllowNotifications = () => {
    Notification.requestPermission().then((permission) => {
      if (permission === "granted") {
        console.log("User allowed notifications");
      } else {
        console.log("User denied notifications");
      }
    });
    setOpen(false); // Close the confirmation dialog
  };

  const handleCancel = () => {
    setOpen(false); // Close the confirmation dialog
  };
  return (
    <DashboardLayout>
      <div className="notifications">
        <h5>Notifications</h5>

        <div className="toggle-radio">
          <input
            type="radio"
            name="rdo"
            id="yes"
            value="yes"
            checked={selectedOption === "yes"}
            onChange={handleOptionChange}
          />
          <input
            type="radio"
            name="rdo"
            id="no"
            value="no"
            checked={selectedOption === "no"}
            onChange={handleOptionChange}
          />
          <div className="switch">
            <label htmlFor="yes" style={{ fontSize: "20px" }}>
              Yes
            </label>
            <label htmlFor="no" style={{ fontSize: "20px" }}>
              No
            </label>
            <span />
          </div>
        </div>
      </div>

      <Modal open={open} onClose={handleCancel}>
        <Box
          sx={{
            display: "flex",
            flexDirection: "column",
            alignItems: "center",
            justifyContent: "center",
            bgcolor: "background.paper",
            p: 4,
            borderRadius: "8px",
            outline: "none",
          }}
        >
          <Typography variant="h6" sx={{ mb: 2 }}>
            Allow Notifications
          </Typography>
          <Typography variant="body1" align="center" sx={{ mb: 3 }}>
            Do you want to allow notifications?
          </Typography>
          <Box sx={{ display: "flex", gap: "16px" }}>
            <MDButton onClick={handleAllowNotifications} variant="contained" color="info">
              OK
            </MDButton>
            <MDButton onClick={handleCancel} variant="contained" color="error">
              Cancel
            </MDButton>
          </Box>
        </Box>
      </Modal>

      <DashboardNavbar />
      <MDBox mt={4}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6} lg={4}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard icon={<CloudIcon />} title="Weather" count="22°C°F" />
            </MDBox>
          </Grid>
          <Grid item xs={12} md={6} lg={4}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="success"
                icon={<AccessTimeIcon />}
                title="Time"
                count={displayTime}
              />
            </MDBox>
          </Grid>

          <Grid item xs={12} md={6} lg={4}>
            <MDBox mb={1.5}>
              <ComplexStatisticsCard
                color="info"
                icon={<CalendarMonthIcon />}
                title="Date"
                count={displayDate}
              />
            </MDBox>
          </Grid>
        </Grid>

        <div className="container">
          <div className="card">
            <div className="buttons">
              <MDButton
                color="info"
                variant="contained"
                onClick={handleDetect}
                disabled={detecting}
              >
                Detect Motion
              </MDButton>
              <MDButton
                color="error"
                variant="contained"
                onClick={handleStopDetect}
                type="button"
                disabled={!detecting}
              >
                Stop Detecting Motion
              </MDButton>
            </div>
            <div className="video-container">
              {detecting && (
                <img
                  ref={myImage}
                  style={{
                    position: "absolute",
                    width: "1438px",
                    height: "578px",
                    zIndex: 1,
                    objectFit: "cover",
                  }}
                  alt="Motion"
                  id="image"
                />
              )}{" "}
              <div className="video">
                <video
                  id="videoElement"
                  playsInline
                  muted
                  ref={myVideo}
                  autoPlay
                  width={1438}
                  height={578}
                  style={{ objectFit: "cover" }}
                />
                <canvas ref={canvasRef} width="1438" height="578" hidden />
              </div>
            </div>
          </div>
        </div>
      </MDBox>
    </DashboardLayout>
  );
}

export default Dashboard;
