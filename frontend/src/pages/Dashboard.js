import React, { useEffect, useState } from "react";
import axios from "axios";
import NavBar from "../components/NavBar";
import './Dashboard.css';

function Dashboard() {
  const [message, setMessage] = useState("");

  useEffect(() => {
    const fetchDashboard = async () => {
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get("http://127.0.0.1:5000/dashboard", {
          headers: { Authorization: `Bearer ${token}` },
        });
        setMessage(response.data.message);
      } catch (err) {
        console.error(err);
        alert("You are not authorized!");
      }
    };

    fetchDashboard();
  }, []);

  return (
      <div>
        <NavBar/>
        <h1>{message}</h1>
      </div>
  );
}

export default Dashboard;
